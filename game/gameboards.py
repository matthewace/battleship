"""Module for the gameboards.  Each player in a game of Battleship has two
gameboards which are each a 10x10 grid of coordinates.  One board is used to
store the player's ship locations and the other is to track attacks of the
opponent's ship-board.
"""
from typing import Optional, Tuple, Union

import game.bitboard as bitboard
from game.ship import Ship


AttackResult = Tuple[bool, bool, Optional[Ship]]
Coordinate = Union[str, bitboard.Coordinate]
CoordinateSet = bitboard.CoordinateSet


PEGS = [HIT, MISS] = ["+", "x"]

Direction = str
DIRECTIONS = {
    "UP": 10,
    "DOWN": -10,
    "RIGHT": 1,
    "LEFT": -1
}

DELTAS_H = [DIRECTIONS["RIGHT"], DIRECTIONS["LEFT"]]
DELTAS_V = [DIRECTIONS["UP"], DIRECTIONS["DOWN"]]
DELTAS_ALL = DELTAS_H + DELTAS_V


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
        self.turn = 0
        self.attacked = CoordinateSet()
        self.hit = CoordinateSet()
        self.miss = CoordinateSet()
        self.occupied = CoordinateSet()
        self.ships = {
            Ship('Carrier'): CoordinateSet(),
            Ship('Battleship'): CoordinateSet(),
            Ship('Destroyer'): CoordinateSet(),
            Ship('Submarine'): CoordinateSet(),
            Ship('Patrol Boat'): CoordinateSet()
        }
        self.symbols = [EMPTY_COORDINATE for _ in range(100)]
        self.sunk = []

    def clear_board(self) -> None:
        """Clear all objects from board."""
        self._clear_board()

    def add_peg(self, coordinate: Coordinate, result: AttackResult) -> None:
        """Add a peg to the board."""
        coordinate = parse_coordinate(coordinate)
        hit, sunk, ship = result
        self.attacked.add(coordinate)
        if hit:
            self.hit.add(coordinate)
            self.ships[ship].add(coordinate)
            peg = ship.symbol()
            if sunk:
                self.sunk.append(peg)
        else:
            self.miss.add(coordinate)
            peg = MISS
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
            self.ships[ship_obj] = ship_coords
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
        result : bool
        """
        coordinate = parse_coordinate(coordinate)
        self.attacked.add(coordinate)
        hit = coordinate in self.occupied
        sunk = False
        ship = None
        if hit:
            self.hit.add(coordinate)
            ship = self.ship_type_at(coordinate)
            if self.check_sunk(ship):
                sunk = True
        else:
            self.miss.add(coordinate)
        return (hit, sunk, ship)

    def check_hit(self, coordinate: Coordinate) -> bool:
        """Check coordinate for Ship and return corresponding Peg."""
        coordinate = parse_coordinate(coordinate)
        return coordinate in self.occupied

    def check_sunk(self, ship_type: Ship) -> bool:
        """Return True if ship_type has been sunk."""
        ship_mask = self.ships[ship_type]
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
        hit, sunk, ship = result
        if hit:
            peg = ship.symbol()
            if sunk:
                self.sunk.append(peg)
        else:
            peg = MISS
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

    def unattacked(self, coordinate: Coordinate) -> bool:
        """Check if coordinate is available to be attacked."""
        coordinate = parse_coordinate(coordinate)
        return coordinate not in self.attacked

    def adjacents(self, coordinate: Coordinate) -> CoordinateSet:
        """Return set of adjacent coordinates."""
        deltas = DIRECTIONS.values()
        mask = bitboard.near_attacks(coordinate, self.attacked,
                                     deltas=deltas, max_d=1)
        return CoordinateSet(mask)

    def ship_attacks(self, ship: Ship) -> CoordinateSet:
        """Return sets of coordinates in which a ship could be attacked."""
        locations = bitboard.CoordinateSet()

        ship_set = self.ships[ship]
        # Skip if no current known coordinates
        if not ship_set or len(ship_set) == len(ship):
            return locations

        # Calculate known coordinates for ship.  We know all coordinates
        # between ship_head and ship_tail should be attacked.
        ship_head = list(ship_set)[0]
        ship_tail = list(ship_set)[-1]
        head_to_tail = bitboard.step_distance(ship_head, ship_tail) + 1
        max_d = len(ship) - head_to_tail
        known_ship = CoordinateSet.ray(ship_head, ship_tail)

        # Return coordinates between head and tail.
        if max_d == 0:
            return known_ship.difference(ship_set)

        deltas = []
        if len(known_ship) == 1:
            deltas = DELTAS_ALL
        else:
            for row in bitboard.BB_ROWS:
                if ship_set.issubset(row):
                    deltas = DELTAS_H
            if not deltas:
                deltas = DELTAS_V

        for coord in known_ship:
            mask = bitboard.near_attacks(coord, self.attacked,
                                         deltas, max_d=max_d)
            locations.update(mask)

        return locations

    def get_ship_attacks(self) -> CoordinateSet:
        """Return a set of potential ship coordinates."""
        ship_attacks = CoordinateSet()
        self.turn += 1
        for ship in self.ships:
            ship_attacks.update(self.ship_attacks(ship))
        return ship_attacks
