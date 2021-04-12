"""Module for the gameboards.  Each player in a game of Battleship has two
gameboards which are each a 10x10 grid of coordinates.  One board is used to
store the player's ship locations and the other is to track attacks of the
opponent's ship-board.
"""
from typing import Optional, Tuple, Union

import bitboard
from gamebox.ship import Ship


AttackResult = Tuple[bool, Optional[Ship]]
Coordinate = Union[str, bitboard.Coordinate]
CoordinateSet = bitboard.CoordinateSet


PEGS = ["x", "o"]

Direction = str
DIRECTIONS = {
    "UP": 10,
    "DOWN": -10,
    "RIGHT": 1,
    "LEFT": -1
}


EMPTY_COORDINATE = '.'


def parse_coordinate(coordinate: Coordinate) -> bitboard.Coordinate:
    """Convert coordinate to `bitboard.Coordinate`."""
    if isinstance(coordinate, str):
        coordinate = bitboard.parse_coordinate(coordinate)
    return coordinate


def ship_coordinates(coordinate: Coordinate,
                     distance: int,
                     direction: str) -> CoordinateSet:
    """Return the coordinates of the head and tail of the ship.

    PARAMS
    ------
    coordinate : Coordinate
        The starting coordinate to place the head of the ship.
    distance : int
        The total number of coordinates to include in set.
    direction : str
        The direction on the grid from bow to tail.

    RETURNS
    -------
    coordinates : CoordinateSet
    """
    coordinate = parse_coordinate(coordinate)
    if coordinate not in bitboard.COORDINATES:
        raise ValueError(f"Invalid bow cooridinate: {coordinate}")
    if direction.upper() not in DIRECTIONS:
        raise ValueError(f"Invalid direction: {direction}")

    delta = DIRECTIONS[direction.upper()]
    tail = coordinate + delta * (distance - 1)
    if tail not in bitboard.COORDINATES:
        raise ValueError(f"Invalid tail coordinate: {tail}")
    return bitboard.CoordinateSet.ray(coordinate, tail)


class GameBoard:
    """A gameboard for the Battleship game."""
    def __init__(self) -> None:
        self._clear_board()

    def __str__(self) -> str:
        out = []
        out.append('+---------------------+\n')
        for coordinate in bitboard.COORDINATES_180:
            bb_coordinate = bitboard.BB_COORDINATES[coordinate]
            if bb_coordinate & bitboard.BB_COL_A:
                out.append('| ')
            out.append(self.symbols[coordinate])
            if bb_coordinate & bitboard.BB_COL_J:
                out.append(f' | {int(coordinate / 10) + 1}\n')
            elif coordinate != bitboard.J1:
                out.append(' ')
        out.append('+---------------------+\n')
        out.append('  A B C D E F G H I J')
        return ''.join(out)

    def _clear_board(self):
        self.attacked = CoordinateSet()
        self.hit = CoordinateSet()
        self.miss = CoordinateSet()
        self.occupied = CoordinateSet()
        self.ships = {
            'Carrier': CoordinateSet(),
            'Battleship': CoordinateSet(),
            'Destroyer': CoordinateSet(),
            'Submarine': CoordinateSet(),
            'Patrol Boat': CoordinateSet()
        }
        self.symbols = [EMPTY_COORDINATE for _ in range(100)]
        self.sunk = []

    def clear_board(self) -> None:
        """Clear all objects from board."""
        self._clear_board()

    def add_peg(self, coordinate: Coordinate, result: AttackResult) -> None:
        """Add a peg to the board."""
        coordinate = parse_coordinate(coordinate)
        hit, ship_type = result
        self.attacked.add(coordinate)
        if hit:
            self.hit.add(coordinate)
            if ship_type:
                peg = ship_type.symbol
                self.sunk.append(peg)
            else:
                peg = PEGS[0]
        else:
            self.miss.add(coordinate)
            peg = PEGS[1]
        self.symbols[coordinate] = peg


class ShipBoard(GameBoard):
    """The board on which a player places their ships.  This should be
    hidden from view from the opponent.
    """

    def add_ship(self,
                 ship_obj: Ship,
                 bow: str,
                 direction: str) -> bool:
        """Add CoordinateSet to board to represent a Ship.

        Params
        ------
        ship_obj : Ship
            The ship to be added to the board.
        bow : Coordinate
            The coordinate of the bow of ship.
        direction : str
            The direction from bow to tail of ship.

        Returns
        -------
        bool
            True if ship added successfully.
        """
        ship_coords = ship_coordinates(bow, len(ship_obj), direction)
        if ship_coords and ship_coords.isdisjoint(self.occupied):
            self.ships[ship_obj.name] = ship_coords
            self.occupied.update(ship_coords)
            for _c in ship_coords:
                self.symbols[_c] = ship_obj.symbol()
            return True
        return False

    def attack_result(self, coordinate: Coordinate) -> AttackResult:
        """Return the results of an attack on `coordinate`.

        Params
        ------
        coordinate : str
            The coordinate being attacked.

        Returns
        -------
        result : AttackResult
            Results of the attack.
            (hit : bool, sunk : bool, ship_type : Ship
        """
        coordinate = parse_coordinate(coordinate)
        hit = coordinate in self.occupied
        ship_type = None
        if hit:
            _ship_type = self.ship_type_at(coordinate)
            if self.check_sunk(_ship_type):
                ship_type = _ship_type
        return (hit, ship_type)

    def check_hit(self, coordinate: Coordinate) -> bool:
        """Check coordinate for Ship and return corresponding Peg."""
        coordinate = parse_coordinate(coordinate)
        return coordinate in self.occupied

    def check_sunk(self, ship_type: Ship) -> bool:
        """Return True if ship_type has been sunk."""
        ship_mask = self.ships[ship_type.name]
        return ship_mask.issubset(self.hit)

    def check_all_sunk(self) -> bool:
        """Return True if all ships have been sunk."""
        return self.occupied == self.hit

    def ship_type_at(self, coordinate: Coordinate) -> Optional[Ship]:
        """Determine which type of ship occupies a provided coordinate.

        PARAMS
        ------
        coordinate : Coordinate
            The coordinate being checked for ship occupancy.

        RETURNS
        -------
        <class `gamebox.ship.Ship`> or None
            Ship object if one is present, else None.
        """
        coordinate = parse_coordinate(coordinate)
        return Ship.from_symbol(self.symbols[coordinate]) or None

    def add_peg(self, coordinate: Coordinate, result: AttackResult) -> None:
        """Add a peg to the board."""
        coordinate = parse_coordinate(coordinate)
        hit, ship_type = result
        self.attacked.add(coordinate)
        if hit:
            self.hit.add(coordinate)
            if ship_type:
                peg = ship_type.symbol
                self.sunk.append(peg)
            else:
                peg = PEGS[0]
        else:
            self.miss.add(coordinate)
            peg = PEGS[1]
        self.symbols[coordinate] = peg.lower()


class AttackBoard(GameBoard):
    """The board on which a player places pegs to mark hit or miss after an
    attack on the opponent's board.

    OPTIONAL PARAMS
    ---------------
    unknown_ship_symbol : str
        The symbol to represent when a ship is hit but unknown
    """

    def __str__(self) -> str:
        return f'Sank: {" ".join(self.sunk)}\n' + super().__str__()
