"""Module for strategies in the game.

https://www.thesprucecrafts.com/how-to-win-at-battleship-411068
https://slate.com/culture/2012/05/how-to-win-at-battleship.html

Ship Placement
    Don't let ships touch
    Typically have one ship on the edge
    Randomness is good

Hunting
    Hunt in diagonals
    Checkerboard method
    Focus fire after hit
    Ship density probability
"""

import game.bitboard as bitboard


Coordinate = bitboard.Coordinate
CoordinateSet = bitboard.CoordinateSet


def focus_fire(coordinate: Coordinate):
    """Search for adjacent Coordinates.

    Params
    ------
    coordinate : Coordinate
    """
    ship_coords = CoordinateSet(coordinate)
    print(ship_coords)
