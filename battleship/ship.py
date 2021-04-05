"""There are 5 ship types in the game of Battleship.  Each ship has a specific
length (number of coordinates).
"""

import dataclasses


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
        return self.symbol() * self.length()

    def symbol(self) -> str:
        """Symbol representation displayed on game board."""
        return self.name[0]

    def length(self) -> int:
        """The amount of coordinates this ship occupies on the game board."""
        return SHIPS[self.name]

    @classmethod
    def from_name(cls, name: str):
        """Create a <class `ship.Ship`> instance from ship name."""
        name = name.capitalize()
        if name in SHIPS:
            return cls(name)
        return None

    @classmethod
    def from_symbol(cls, symbol: str):
        """Creates a <class `ship.Ship`> instance from ship symbol."""
        symbol = symbol.upper()
        for name in SHIPS:
            if symbol == name[0]:
                return cls(name)
        return None

    @classmethod
    def build(cls, name: str):
        """Creates a <class `ship.Ship`> instance from either ship symbol or
        name.
        """
        return cls.from_name(name) or cls.from_symbol(name)
