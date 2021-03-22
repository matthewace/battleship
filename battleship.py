"""Module containing all the classes needed to play a game of BATTLESHIP.

At some point I may try and split this up into separate modules, however for
now everything is in one spot for simplicity.

Exceptions:
    InvalidCoordinate, InvalidCoordinates
Exported Classes:
    Ship, Player, CPU

Future plans:
    - Add CPU logic and difficulty settings
"""

import dataclasses
import random

from enum import Enum
from typing import Iterator, List, Optional, Tuple


ROW_NAMES = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
COL_NAMES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

Coordinate = int
COORDINATES = [    
    A1,  B1,  C1,  D1,  E1,  F1,  G1,  H1,  I1,  J1,
    A2,  B2,  C2,  D2,  E2,  F2,  G2,  H2,  I2,  J2,
    A3,  B3,  C3,  D3,  E3,  F3,  G3,  H3,  I3,  J3,
    A4,  B4,  C4,  D4,  E4,  F4,  G4,  H4,  I4,  J4,
    A5,  B5,  C5,  D5,  E5,  F5,  G5,  H5,  I5,  J5,
    A6,  B6,  C6,  D6,  E6,  F6,  G6,  H6,  I6,  J6,
    A7,  B7,  C7,  D7,  E7,  F7,  G7,  H7,  I7,  J7,
    A8,  B8,  C8,  D8,  E8,  F8,  G8,  H8,  I8,  J8,
    A9,  B9,  C9,  D9,  E9,  F9,  G9,  H9,  I9,  J9,
    A10, B10, C10, D10, E10, F10, G10, H10, I10, J10    
] = range(100)
COORDINATE_NAMES =  [c + r for r in ROW_NAMES for c in COL_NAMES]


def parse_coordinate(name: str) -> Coordinate:
    """Get coordinate value from name"""
    return COORDINATE_NAMES.index(name)


def coordinate_name(coordinate: Coordinate) -> str:
    """Get name of coordinate from tuple values"""
    return COORDINATE_NAMES[coordinate]


def coordinate_row(coordinate: Coordinate) -> int:
    """Get index of coordinate's row where ``0`` is row 1, ``9`` is row 10"""
    return int(coordinate / 10)


def coordinate_column(coordinate: Coordinate) -> int:
    """Get index of coordinate's column where ``0`` is column A."""
    return int(coordinate % 10)


def coordinate_mirror(coordinate: Coordinate) -> Coordinate:
    """Returns the index of the mirrored coordinate"""
    return 90 - 10 * coordinate_row(coordinate) + coordinate_column(coordinate)


COORDINATES_180 = [coordinate_mirror(c) for c in COORDINATES]


Bitboard = int
BB_EMPTY = 0
BB_ALL = 0x000f_ffff_ffff_ffff_ffff_ffff_ffff

BB_COORDINATES = [
    BB_A1,  BB_B1,  BB_C1,  BB_D1,  BB_E1,  BB_F1,  BB_G1,  BB_H1,  BB_I1,  BB_J1,
    BB_A2,  BB_B2,  BB_C2,  BB_D2,  BB_E2,  BB_F2,  BB_G2,  BB_H2,  BB_I2,  BB_J2,
    BB_A3,  BB_B3,  BB_C3,  BB_D3,  BB_E3,  BB_F3,  BB_G3,  BB_H3,  BB_I3,  BB_J3,
    BB_A4,  BB_B4,  BB_C4,  BB_D4,  BB_E4,  BB_F4,  BB_G4,  BB_H4,  BB_I4,  BB_J4,
    BB_A5,  BB_B5,  BB_C5,  BB_D5,  BB_E5,  BB_F5,  BB_G5,  BB_H5,  BB_I5,  BB_J5,
    BB_A6,  BB_B6,  BB_C6,  BB_D6,  BB_E6,  BB_F6,  BB_G6,  BB_H6,  BB_I6,  BB_J6,
    BB_A7,  BB_B7,  BB_C7,  BB_D7,  BB_E7,  BB_F7,  BB_G7,  BB_H7,  BB_I7,  BB_J7,
    BB_A8,  BB_B8,  BB_C8,  BB_D8,  BB_E8,  BB_F8,  BB_G8,  BB_H8,  BB_I8,  BB_J8,
    BB_A9,  BB_B9,  BB_C9,  BB_D9,  BB_E9,  BB_F9,  BB_G9,  BB_H9,  BB_I9,  BB_J9,
    BB_A10, BB_B10, BB_C10, BB_D10, BB_E10, BB_F10, BB_G10, BB_H10, BB_I10, BB_J10
] = [1 << c for c in COORDINATES]

BB_COLS = [
    BB_COL_A,
    BB_COL_B,
    BB_COL_C,
    BB_COL_D,
    BB_COL_E,
    BB_COL_F,
    BB_COL_G,
    BB_COL_H,
    BB_COL_I,
    BB_COL_J,
] = [0x0401_0040_1004_0100_4010_0401 << i for i in range(10)]

BB_ROWS = [
    BB_ROW_1,
    BB_ROW_2,
    BB_ROW_3,
    BB_ROW_4,
    BB_ROW_5,
    BB_ROW_6,
    BB_ROW_7,
    BB_ROW_8,
    BB_ROW_9,
    BB_ROW_10,
] = [0x03ff << 10 * i for i in range(10)]

BB_PERIMETER = BB_ROW_1 | BB_ROW_10 | BB_COL_A | BB_COL_J
BB_SIDES = BB_COL_A | BB_COL_J
BB_TOP_BOTTOM = BB_ROW_1 | BB_ROW_10

def lsb(bb: Bitboard) -> int:
    return (bb & -bb).bit_length() - 1

def scan_forward(bb: Bitboard) -> Iterator[Coordinate]:
    while bb:
        r = bb & -bb
        yield r.bit_length() - 1
        bb ^= r

def msb(bb: Bitboard) -> int:
    return bb.bit_length() - 1

def scan_reversed(bb: Bitboard) -> Iterator[Coordinate]:
    while bb:
        r = bb.bit_length() - 1
        yield r
        bb ^= BB_COORDINATES[r]

def cross_edge(bb: Bitboard) -> bool:
    """Test if a provided mask (useful only for testing Ship masks) crosses
    edges which would not be a legal placement.
    """
    return (bb & BB_ROW_1 and bb & BB_ROW_10 or
            bb & BB_COL_A and bb & BB_COL_J)



class InvalidCoordinates(Exception):
    def __init__(self, coordinates: List[Coordinate]) -> None:
        self.coordinates = coordinates

    def __str__(self):
        return f'InvalidCoordinates({self.coordinates})'


class InvalidCoordinate(Exception):
    def __init__(self, coordinate: Coordinate) -> None:
        self.coordinate = coordinate

    def __str__(self) -> str:
        return f'InvalidCoordinate({self.coordinate})'


class ShipType(Enum):
    PATROLBOAT = 0
    SUBMARINE = 1
    DESTROYER = 2
    BATTLESHIP = 3
    CARRIER = 4

SHIP_SYMBOLS = ['P', 'S', 'D', 'B', 'C']
SHIP_NAMES = ['Patrol Boat', 'Submarine', 'Destroyer', 'Battleship', 'Carrier']
SHIP_LENGTHS = [2, 3, 3, 4, 5]

def ship_symbol(ship_type: ShipType) -> Optional[str]:
    return SHIP_SYMBOLS[ship_type.value] if ship_type else None

def ship_name(ship_type: ShipType) -> Optional[str]:
    return SHIP_NAMES[ship_type.value] if ship_type else None

def ship_length(ship_type: ShipType) -> Optional[int]:
    return SHIP_LENGTHS[ship_type.value] if ship_type else None

def get_ship_type(name: str) -> ShipType:
    if name in SHIP_SYMBOLS:
        return ShipType(SHIP_SYMBOLS.index(name))
    if name in SHIP_NAMES:
        return ShipType(SHIP_NAMES.index(name))
    return None


class Heading(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3

HEADING_SYMBOLS = ['N', 'S', 'E', 'W']
HEADING_NAMES = ["North", "South", "East", "West"]
HEADING_DELTAS = [-10, 10, -1, 1]

def heading_symbol(heading: Heading) -> str:
    return HEADING_SYMBOLS[heading.value]

def heading_name(heading: Heading) -> str:
    return HEADING_NAMES[heading.value]

def heading_delta(heading: Heading) -> int:
    return HEADING_DELTAS[heading.value]

def parse_heading(direction: str) -> Heading:
    if direction in HEADING_SYMBOLS:
        return Heading(HEADING_SYMBOLS.index(direction))
    if direction in HEADING_NAMES:
        return Heading(HEADING_NAMES.index(direction))
    return None

def ship_coordinates(name: str, bow: str, heading: str) -> List[Coordinate]:
    """Identifies the coordinates of a ShipType provided a bow and heading.

    Parameters
    ----------
    ship_type: str
        The type of ship.
    bow: str
        The initial coordinate indicating the bow of the Ship.
    heading: str
        The direction in which the ship is facing.

    Returns
    -------
    coordinates: List[board.Coordinate]
        All coordinates occupied by the ShipType.
    """
    ship_type = get_ship_type(name)
    bow = parse_coordinate(bow)
    delta = heading_delta(parse_heading(heading))
    coordinates = []    

    for i in range(ship_length(ship_type)):
        coordinate = bow + i * delta
        if coordinate not in COORDINATES:
            raise InvalidCoordinates(coordinate)
        coordinates.append(coordinate)

    return coordinates

@dataclasses.dataclass(frozen=True)
class Ship:
    name: str
    mask: Bitboard

    def __str__(self) -> str:
        return self.symbol

    def __len__(self):
        """The length of the Ship."""
        return ship_length(parse_ship_type(self.symbol))

    @classmethod
    def build(cls, name: str, bow: str, heading: str):
        """Returns a <class `battleship.Ship`> instance."""
        coordinates = ship_coordinates(name, bow, heading)
        mask = CoordinateSet(coordinates).mask
        if cross_edge(mask):
            raise InvalidCoordinates(coordinates)

        return cls(ship_name(get_ship_type(name)), mask)


EMPTY_FEN = "0/0/0/0/0/0/0/0/0/0/0"

class BaseBoard:
    """Game is played on a 10x10 grid.  Columns are denoted by letters A-J and
    rows are denoted by numbers 1-10.  
    
    . . . . . . . . . . 10
    . . . . . . . . . . 9
    . . . . . . . . . . 8
    . . . . . . . . . . 7
    . . . . . . . . . . 6
    . . . . . . . . . . 5
    . . . . . . . . . . 4
    . . . . . . . . . . 3
    . . . . . . . . . . 2
    . . . . . . . . . . 1
    A B C D E F G H I J

    A `fen` is a stolen chess term but I like it so we'll use it here.  The fen
    is a notation for the layout of the coordinates on the grid.  There are 10
    segments separated by a `/`.  Each segment represents a row on the grid.
    A number represents the amount of consecutive empty coordinates, and any
    other character represents another object on the board.

    TODO: Implement a FEN
    """
    def __init__(self) -> None:
        self.log = []
        self.game_num = 0
        self._reset_board()

    def __str__(self) -> str:
        coordinates = ['.' for _ in COORDINATES]
        # Add ships
        for name, bb in self.ships.items():
            symbol = name[0]
            for c in scan_forward(bb):
                coordinates[c] = symbol
        # Add hits
        for c in scan_forward(self.hit):
            coordinates[c] = coordinates[c].lower()
        # Add Misses
        for c in scan_forward(self.miss):
            coordinates[c] = 'x'

        out = '+---------------------+\n'
        out += '| '
        for c in COORDINATES_180:
            mask = BB_COORDINATES[c]
            out += coordinates[c]
            if mask & BB_COL_J:
                out += f' | {int(c / 10) + 1}'
                if c == J1:
                    out += '\n+'
                else:
                    out += '\n| '
            else:
                out += ' '
        out += '---------------------+\n'
        out += '  A B C D E F G H I J'
        return out            

    def _reset_board(self) -> None:
        self.game_num += 1
        self.turn_num = 0

        self.attacked = BB_EMPTY
        self.hit = BB_EMPTY
        self.miss = BB_EMPTY

        self.occupied = BB_EMPTY
        self.ships = {
            'Carrier': BB_EMPTY,
            'Battleship': BB_EMPTY,
            'Destroyer': BB_EMPTY,
            'Submarine': BB_EMPTY,
            'Patrol Boat': BB_EMPTY
        }

        self._update_fen()
        self.log.append(f'Game Number {self.game_num}:')

    def clear_board(self) -> None:
        """Resets the board to empty"""
        self._reset_board()

    def _update_fen(self) -> None:
        """Update the fen based on current board"""
        pass

    def update_fen(self) -> None:
        self._update_fen()


class ShipBoard(BaseBoard):
    def _add_ship(self, ship: Ship) -> bool:
        """Attempt to add a ship to the board.

        Parameters
        ----------
        ship: Ship
            The ship to be added
        
        Returns
        -------
        ship_added: bool
            True if ship is added to board, False if coordinates are occupied
            or ship object is invalid.
        """
        if ship.name not in self.ships or ship.mask & self.occupied:
            return False

        self.ships[ship.name] = ship.mask
        self.occupied |= ship.mask
        return True

    def add_ship(self, ship: Ship) -> bool:
        return self._add_ship(ship)

    def ship_type_at(self, coordinate: Coordinate) -> Optional[ShipType]:
        """Find the type of ship (if one exists) at a coordinate"""
        bb_mask = BB_COORDINATES[coordinate] & BB_ALL
        for name, mask in self.ships.items():
            if mask & bb_mask:
                return get_ship_type(name)
        return None

    def attack(self, coordinate: str) -> str:
        """Attack the provided coordinate and return True for hit and False
        for miss.
        """
        if coordinate in COORDINATE_NAMES:
            coordinate = parse_coordinate(coordinate)
        return self._attack(coordinate)

    def _attack(self, coordinate: Coordinate) -> str:
        reply = "MISS"
        mask = BB_COORDINATES[coordinate]
        ship_type = self.ship_type_at(coordinate)

        if ship_type:
            reply = "HIT!"
            self.hit |= mask
            if self.ded_ship(ship_type):
                reply += f'  You Sank My {ship_name(ship_type)}!!!'
        else:
            self.miss |= mask

        self.attacked |= mask
        return reply

    def ded_ship(self, ship_type: ShipType) -> bool:
        """Verify if the ship is ded"""
        ship_bb = self.ships[ship_name(ship_type)]
        return ship_bb & self.hit == ship_bb

    def all_ded_ships(self) -> bool:
        """Check if all ships are dead"""
        return self.occupied == self.hit


class AttackBoard(BaseBoard):
    def __str__(self) -> str:
        coordinates = ['.' for _ in COORDINATES]
        
        # Add hits
        for c in scan_forward(self.hit):
            coordinates[c] = 'o'
        # Add Misses
        for c in scan_forward(self.miss):
            coordinates[c] = 'x'

        out = '+---------------------+\n'
        out += '| '
        for c in COORDINATES_180:
            mask = BB_COORDINATES[c]
            out += coordinates[c]
            if mask & BB_COL_J:
                out += f' | {int(c / 10) + 1}'
                if c == J1:
                    out += '\n+'
                else:
                    out += '\n| '
            else:
                out += ' '
        out += '---------------------+\n'
        out += '  A B C D E F G H I J'
        return out

    def _reset_board(self) -> None:
        self.game_num += 1
        self.turn_num = 0

        self.hit = BB_EMPTY
        self.miss = BB_EMPTY
        self.attacked = BB_EMPTY

    def _attack(self, coordinate: Coordinate, hit: bool) -> None:
        mask = BB_COORDINATES[coordinate]
        self.attacked |= mask
        if hit:
            self.hit |= mask
        else:
            self.miss |= mask

    def attack(self, coordinate: Coordinate, hit: bool) -> None:
        """Add `hit` or `miss` peg to board"""
        if coordinate in COORDINATE_NAMES:
            coordinate = parse_coordinate(coordinate)
        self._attack(coordinate, hit) 

    def _is_attacked(self, coordinate: Coordinate) -> bool:
        """Check if coordinate has already been attacked"""
        return BB_COORDINATES[coordinate] & self.attacked

    def is_attacked(self, coordinate: Coordinate) -> bool:
        if type(coordinate) == str:
            coordinate = parse_coordinate(coordinate)
        return self._is_attacked(coordinate)


class CoordinateSet:
    """A set of coordinates"""
    def __init__(self, coordinates: list) -> None:
        try:
            self.mask = coordinates & BB_ALL
            return
        except:
            self.mask = 0

        for coordinate in coordinates:
            self.add(coordinate)

    def __str__(self) -> str:
        out = ''

        for coord in COORDINATES_180:
            mask = BB_COORDINATES[coord]
            out += '1' if self.mask & mask else '.'

            if not mask & BB_COL_J:
                out += ' '
            elif coord != J1:
                out += '\n'

        return out

    def add(self, coordinate: Coordinate) -> None:
        self.mask |= BB_COORDINATES[coordinate]


class Player:
    """A class to represent one of the 2 players in the game"""
    def __init__(self, name: str) -> None:
        self.name = name
        self.ship_board = ShipBoard()
        self.attack_board = AttackBoard()

        self.wins = 0
        self.losses = 0
        self.hits = 0
        self.attacks = 0

        self._clear_boards()

    def __str__(self) -> str:
        return f'{self.name}'

    def accuracy(self) -> float:
        try:
            return round(self.hits * 100 / self.attacks, 2)
        except:
            return 0.00

    def stats(self) -> str:
        stats = [
            f"Record: {self.wins} - {self.losses}",
            f"Accuracy: {self.accuracy()} ({self.hits}/{self.attacks})"
        ]
        return '\n'.join(stats)

    def _clear_boards(self) -> None:
        self.ship_board.clear_board()
        self.attack_board.clear_board()

    def clear_boards(self) -> None:
        """Reset the game boards back to default state (empty)."""
        self._clear_boards()

    def _show_board(self, board: BaseBoard) -> None:
        print(board)

    def show_ship_board(self) -> None:
        self._show_board(self.ship_board)

    def show_attack_board(self) -> None:
        self._show_board(self.attack_board)

    def show_boards(self) -> None:
        self.show_attack_board()
        print()
        self.show_ship_board()

    def _add_ship(self, ship: Ship) -> bool:
        return self.ship_board.add_ship(ship)

    def add_ship(self, ship: Ship) -> bool:
        """Add a ship to the board

        Parameters
        ----------
        ship : <class battleship.Ship>

        Returns
        -------
        success : bool
        """
        return self._add_ship(ship)

    def _get_rekt(self, coordinate) -> str:
        return self.ship_board.attack(coordinate)

    def get_rekt(self, coordinate) -> str:
        """Check if attack at coordinate hits your ShipBoard"""
        return self._get_rekt(coordinate)

    def is_dead(self) -> bool:
        """Check if all ships are ded"""
        return self._is_dead()

    def _is_dead(self) -> bool:
        return self.ship_board.all_ded_ships()

    def add_attack_peg(self, coordinate: Coordinate, hit: bool) -> None:
        """Updates attack board with appropriate symbol based on hit or not"""
        if coordinate in COORDINATE_NAMES:
            coordinate = parse_coordinate(coordinate)
        self._add_attack_peg(coordinate, hit)

    def _add_attack_peg(self, coordinate: Coordinate, hit: bool) -> None:
        self.attacks += 1
        if hit:
            self.hits += 1
        self.attack_board.attack(coordinate, hit)

    def win(self) -> None:
        """Add to the WIN column!"""
        self.wins += 1

    def lose(self) -> None:
        """Add to the LOSE column :( """
        self.losses += 1


class CPU(Player):
    """A computer opponent whose choices are all randomized.  Maybe we'll get
    around to adding logic to the choices...
    """
    def add_ship(self, ship_type: ShipType) -> bool:
        """Add a ship using random bow and heading"""
        return self._add_ship(ship_type)

    def _add_ship(self, ship_type: ShipType) -> bool:
        symbol = ship_symbol(ship_type)
        attempts = 0
        while True:
            attempts += 1
            bow = random.choice(COORDINATE_NAMES)
            heading = random.choice(HEADING_NAMES)
            try:
                if self.ship_board.add_ship(Ship.build(symbol, bow, heading)):
                    print(attempts)
                    return True
            except:
                pass
            if attempts > 50:
                return False

    def add_all_ships(self) -> bool:
        """Add all ships to board"""
        return self._add_all_ships()

    def _add_all_ships(self) -> bool:
        for ship_type in ShipType:
            if not self._add_ship(ship_type):
                return False
        return True

    def _choose_attack_coordinate(self) -> str:
        while True:
            coord = random.choice(COORDINATES)
            if not self.attack_board._is_attacked(coord):
                return coordinate_name(coord)

    def choose_attack_coordinate(self) -> str:
        return self._choose_attack_coordinate()
