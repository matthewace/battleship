"""There are 5 ship types in the game of Battleship.  Each ship has a specific
length (number of coordinates).
"""

import dataclasses
from typing import Iterator


ShipType = int

SHIPS = {
    "Carrier": 5,
    "Battleship": 4,
    "Submarine": 3,
    "Destroyer": 3,
    "Patrol Boat": 2
}


@dataclasses.dataclass(frozen=True)
class Ship:
    """A dataclass representation of a Ship.

    Attributes:
    -----------
    name : str
        The name of the ship which represents its type.
    """
    name: str

    def __str__(self) -> str:
        return self.name

    def __len__(self) -> int:
        """The amount of coordinates this ship occupies on the game board."""
        return SHIPS[self.name]

    def symbol(self) -> str:
        """Symbol representation displayed on game board."""
        return self.name[0]

    @classmethod
    def from_symbol(cls, symbol: str):
        """Creates a <class `ship.Ship`> instance from ship symbol."""
        symbol = symbol.upper()
        for name in SHIPS:
            if symbol == name[0]:
                return cls(name)
        return None


@dataclasses.dataclass(frozen=True)
class ShipSet:
    """A collection of all the types of Ship that is needed for a game of
    Battleship.
    """
    ships = (Ship(name) for name in SHIPS)

    def __iter__(self) -> Iterator[Ship]:
        for ship in self.ships:
            yield ship
