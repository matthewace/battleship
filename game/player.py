"""Module for the Player and CPU classes.

Exported
--------
Player - Human player
CPU - AI player
"""
import random
from typing import Dict, List, Tuple

import game.bitboard as bitboard
from game.gameboards import AttackBoard, ShipBoard
from game.ship import Ship


AttackResult = Tuple[bool, Ship]

COORDINATES = bitboard.COORDINATE_NAMES
ODD_COORDS = bitboard.CoordinateSet(bitboard.BB_ODDS)


CHOICES = {
    "coordinate": bitboard.COORDINATE_NAMES,
    "direction": ["UP", "DOWN", "LEFT", "RIGHT"],
}


def get_probabilities(items: List[object]) -> Dict[int, List[object]]:
    """Calculate percent probability of each unique object in list."""
    probabilities = {}
    items.sort()
    #  total_items = len(items)
    while items:
        item = items[0]
        num_item = items.count(item)
        item_prob = num_item  # int(100 * num_item / total_items)
        if item_prob not in probabilities:
            probabilities[item_prob] = []
        probabilities[item_prob].append(item)
        items = items[num_item:]
    return probabilities


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

        self.clear_boards()
        self.set_ships_placed(False)

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
        self.attack_board = AttackBoard()
        self.ship_board = ShipBoard()

    def set_ships_placed(self, all_placed: bool) -> None:
        """Update ships_placed variable."""
        self.ships_placed = all_placed

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
        hit = result[0]
        self.attacks += 1
        if hit:
            self.hits += 1
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

    def _attack_options(self) -> List[str]:
        """Return a list of coordinate names which have not been attacked."""
        unattacked = ~self.attack_board.attacked
        return [bitboard.COORDINATE_NAMES[i] for i in unattacked]

    def is_dead(self) -> bool:
        """Return True if all player's ships are sunk."""
        return self.ship_board.check_all_sunk()

    def win(self) -> None:
        """Add to the WIN column."""
        self.wins += 1

    def lose(self) -> None:
        """Add to the LOSS column."""
        self.losses += 1


class Human(Player):
    """The human variant of a Player."""

    @staticmethod
    def choose_direction() -> str:
        """Prompt Player for choice of direction."""
        options = ["UP", "DOWN", "LEFT", "RIGHT"]
        choice = ''
        while choice not in options and "Q" not in choice:
            choice = input('Choose Direction: ').upper()
        return choice

    def choose_coordinate(self) -> str:
        """Prompt player to choose a coordinate."""
        options = self._attack_options()
        choice = ''
        while choice not in options and "Q" not in choice:
            choice = input('Choose Coordinate: ').upper()
        return choice


class CPU(Player):
    """The AI variant of a Player."""

    def __init__(self, name: str, level: int = 0) -> None:
        super().__init__(name)
        self.level = level

    def _attack_options(self) -> List[str]:
        """Return a list of coordinate names which have not been attacked."""
        options = ~self.attack_board.attacked
        if self.ships_placed and self.level > 0:
            ship_attacks = self._get_ship_attacks()
            if ship_attacks:
                options = ship_attacks
            elif self.level == 3:
                densities = self.attack_board.ship_densities()
                prob_table = get_probabilities(densities)
                top_prob = sorted(prob_table)[-1]
                options = [i for i in prob_table[top_prob] if i in ODD_COORDS]
                if not options:
                    options = prob_table[top_prob]
            elif self.level == 2:
                options.intersection_update(ODD_COORDS)
        return [COORDINATES[i] for i in options]

    def _get_ship_attacks(self) -> bitboard.CoordinateSet:
        return self.attack_board.get_ship_attacks()

    def choose_coordinate(self) -> str:
        """Choose an attack coordinate."""
        options = self._attack_options()
        return random.choice(options)

    @staticmethod
    def choose_direction() -> str:
        """Randomly choose of direction."""
        options = ["UP", "DOWN", "LEFT", "RIGHT"]
        return random.choice(options)
