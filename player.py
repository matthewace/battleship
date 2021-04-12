"""Module for the Player and CPU classes.

Exported
--------
Player - Human player
CPU - AI player
"""
import random
from typing import Tuple

import bitboard
from gamebox import AttackBoard, ShipBoard, Ship


AttackResult = Tuple[bool, Ship]

CHOICES = {
    "coordinate": bitboard.COORDINATE_NAMES,
    "direction": ["UP", "DOWN", "LEFT", "RIGHT"],
}


class Player:
    """The human player."""

    def __init__(self, name: str) -> None:
        """Initialize a Player.

        Params
        ------
        name : str
            Player's name
        """
        self.name = name
        self.wins = 0
        self.losses = 0

        self.hits = 0
        self.attacks = 0

        self.attack_board = AttackBoard()
        self.ship_board = ShipBoard()

    def __str__(self) -> str:
        return f"{self.name} {self.record()} {self.accuracy()}%"

    def record(self) -> str:
        """Return the player's win-loss record."""
        return f"({self.wins} - {self.losses})"

    def accuracy(self) -> float:
        """Return the player's accuracy: (hits/attacks) * 100"""
        if self.attacks == 0:
            return 0.0
        return round(self.hits * 100 / self.attacks, 1)

    def clear_boards(self) -> None:
        """Clear boards for a new game."""
        self.attack_board.clear_board()
        self.ship_board.clear_board()

    def show_attack_board(self) -> None:
        """Print attack board."""
        print(self.attack_board)

    def show_ship_board(self) -> None:
        """Print ship board."""
        print(self.ship_board)

    def show_boards(self) -> None:
        """Print the player's boards."""
        self.show_attack_board()
        self.show_ship_board()

    def add_ship(self, ship_obj: Ship, bow: str, direction: str) -> bool:
        """Add a Ship to the player's ShipBoard.

        Params
        ------
        ship_obj : Ship
            The ship to be added to the board.
        bow : Coordinate
            The coordinate of the bow of ship.
        direction : str
            The direction from bow to tail of ship.
        """
        return self.ship_board.add_ship(ship_obj, bow, direction)

    def attacked(self, coordinate: str) -> AttackResult:
        """Check if an attack hits player's ShipBoard.

        Params
        ------
        coordinate : str
            The coordinate being attacked.

        Returns
        -------
        result : AttackResult
            Results of the attack.
            (hit : bool, ship_type : Ship)
        """
        return self.ship_board.attack_result(coordinate)

    def add_attack_peg(self, coordinate: str, result: AttackResult) -> None:
        """Add peg to AttackBoard based on results of attack.

        Params
        ------
        coordinate : str
            The attacked coordinate.
        results : AttackResult
            The results of attacking coordinate.
        """
        self.attack_board.add_peg(coordinate, result)

    def add_ship_peg(self, coordinate: str, result: AttackResult) -> None:
        """Add peg to ShipBoard based on results of attack.

        Params
        ------
        coordinate : str
            The attacked coordinate.
        results : AttackResult
            The results of attacking coordinate.
        """
        self.ship_board.add_peg(coordinate, result)

    def is_dead(self) -> bool:
        """Return True if all player's ships are sunk."""
        return self.ship_board.check_all_sunk()

    def win(self) -> None:
        """Add to the WIN column."""
        self.wins += 1

    def lose(self) -> None:
        """Add to the LOSS column."""
        self.losses += 1

    # User input methods
    @staticmethod
    def choose(choice_type: str) -> str:
        """Get player's choice of available options.

        Params
        ------
        choice_type : str
            Key for list of choices.
        """
        options = CHOICES[choice_type.lower()]
        tries = 0
        while tries < 5:
            tries += 1
            choice = input(f'Choose a {choice_type}: ')
            if choice.upper() in options:
                return choice
        return None


class CPU(Player):
    """The AI variant of a Player."""

    # User input methods
    @staticmethod
    def choose(choice_type: str) -> str:
        options = CHOICES[choice_type.lower()]
        return random.choice(options)
