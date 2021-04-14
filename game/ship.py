"""There are 5 ship types in the game of Battleship.  Each ship has a specific
length (number of coordinates).
"""

import dataclasses


ShipType = int
SHIPS = [CARRIER, BATTLESHIP, SUBMARINE, DESTROYER, PATROLBOAT] = range(5)
SHIP_NAMES = ["Carrier", "Battleship", "Submarine", "Destroyer", "Patrol Boat"]
SHIP_SYMBOLS = ["C", "B", "S", "D", "P"]
SHIP_LENGTHS = [5, 4, 3, 3, 2]


@dataclasses.dataclass(frozen=True)
class Ship:
    """A dataclass representation of a Ship.

    Attributes:
    -----------
    name : str
        Name of Ship.
    """
    name: str

    def __str__(self) -> str:
        return self.name

    def __len__(self) -> int:
        """The amount of coordinates this ship occupies on the game board."""
        return SHIP_LENGTHS[self.ship_type()]

    def symbol(self) -> str:
        """Symbol representation displayed on game board."""
        return SHIP_SYMBOLS[self.ship_type()]

    def ship_type(self) -> ShipType:
        """Return the ShipType."""
        return SHIP_NAMES.index(self.name)

    @classmethod
    def from_symbol(cls, symbol: str):
        """Create a `Ship` instance from ship symbol."""
        name = SHIP_NAMES[SHIP_SYMBOLS.index(symbol.upper())]
        return cls(name)

    @classmethod
    def from_type(cls, ship_type: ShipType):
        """Create a `Ship` instance from ShipType."""
        return cls(SHIP_NAMES[ship_type])
