"""Module for the gameboards.  Each player in a game of Battleship has two
gameboards which are each a 10x10 grid of coordinates.  One board is used to
store the player's ship locations and the other is to track attacks of the
opponent's ship-board.
"""

import bitboard


HIT = 'x'
MISS = 'o'


# Functions from bitboard
CoordinateSet = bitboard.CoordinateSet


def mask(coordinate: str) -> bitboard.Bitboard:
    c = bitboard.parse_coordinate(coordinate)
    return bitboard.BB_COORDINATES[c]


class GameBoard:
    """A gameboard for the Battleship game."""
    def __init__(self):
        self._clear_board()

    def _clear_board(self):
        self.attacked = CoordinateSet.empty()
        self.hit = CoordinateSet.empty()
        self.miss = CoordinateSet.empty()

        self.occupied = CoordinateSet.empty()
        self.ships = {
            'Carrier': CoordinateSet.empty(),
            'Battleship': CoordinateSet.empty(),
            'Destroyer': CoordinateSet.empty(),
            'Submarine': CoordinateSet.empty(),
            'Patrol Boat': CoordinateSet.empty()
        }

    def clear_board(self) -> None:
        """Clear all CoordinateSet objects of board."""
        self._clear_board()

    def place_peg(self, coordinate: str, hit: bool) -> None:
        """Mark the board with a HIT or MISS symbol.

        Parameters
        ----------
        coordinate : str
            The coordinate in {COL}{ROW} format; ie "A1" or "H3"

        hit : bool
            Whether the marker is HIT (True) or MISS (False)
        """
        bb_coord = mask(coordinate)
        self.occupied |= bb_coord
        if hit:
            self.hit |= bb_coord
        else:
            self.miss |= bb_coord
