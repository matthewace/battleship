"""Module which contains the game."""

import os
from typing import List, Tuple, Union

from game.player import Human, Player


GameResult = Tuple[Player, Player]
Log = List[Union[str, List[str]]]


def stringify(logs: Log, indent: int = 4, level: int = 0) -> str:
    """Turn logs into string format for printing.

    Params
    ------
    logs : Log
        A list of str or other Log lists to be stringified.
    indent : int
        Optional: The number of spaces to indent per level.
    level : int
        Optional: The current level in logs to set indent.

    Returns
    -------
    pretty_logs : str
        The logs in printable format.
    """
    pretty_logs = ''
    tabs = ' ' * indent * level
    level += 1
    for log in logs:
        if isinstance(log, str):
            pretty_logs += f"{tabs}{log}\n"
        else:
            pretty_logs += stringify(log, level=level, indent=indent)
    return pretty_logs


def place_ships(player: Player) -> Log:
    """Guide player in placing ships on board."""
    log = []
    log.append(f"FUNC: place_ships({player.name})")
    for ship in player.ship_board.ships:
        ship_log = []
        ship_log.append(f"Building {ship}")
        built = False
        while not built:
            build_log = []
            if isinstance(player, Human):
                os.system('clear')
                print(f'*** Building {ship} ***')
                player.show_ship_board()
                print(f'Ship Length: {len(ship)}')
            bow = player.choose("coordinate").upper()
            direction = player.choose("direction").upper()
            try:
                build_log.append(f"add_ship({ship}, {bow}, {direction})")
                built = player.add_ship(ship, bow, direction)
            except ValueError as err:
                build_log.append(f"ERROR: {err}")
            ship_log.append(build_log)
        log.append(ship_log)
    return log


class Battleship:
    """A game of Battleship."""

    def __init__(self, player1: Player, player2: Player) -> None:
        self.player1 = player1
        self.player2 = player2
        self.players = [self.player1, self.player2]

        self.turn_num = 0
        self.half_turn = 0
        self.logs = {"turns": [], "debug": []}

        self.logs["turns"].append(f"P1: {self.player1} | P2: {self.player2}")
        self.set_boards()

    def play_game(self) -> GameResult:
        """Manage the gameplay.

        Returns
        -------
        result : GameResult
            (winner, loser)
        """
        os.system('clear')
        winner = None
        loser = None
        turn_log = f"P1: {self.player1} | P2: {self.player2}"
        while winner is None:
            if self.half_turn == 0:
                self.turn_num += 1
                if self.turn_num > 100:
                    break
                self.logs["turns"].append(turn_log)
                self.logs["turns"].append(f"Turn {self.turn_num}:")
                turn_log = []
            attacker = self.players[self.half_turn]
            defender = self.players[self.half_turn - 1]
            if isinstance(attacker, Human):
                os.system('clear')
                print(f"{attacker.name}'s turn to attack.")
                attacker.show_boards()
            valid_choice = False
            while not valid_choice:
                attk_coord = attacker.choose("coordinate")
                if 'Q' in attk_coord:
                    turn_log.append(f"{attacker.name} forfeits...")
                    self.logs["turns"].append(turn_log)
                    winner = defender
                    loser = attacker
                    break
                valid_choice = attacker.attack_board.unattacked(attk_coord)
            result = defender.attacked(attk_coord)
            defender.add_ship_peg(attk_coord, result)
            attacker.add_attack_peg(attk_coord, result)
            hit, sunk, ship = result
            shot_log = []
            shot_log.append(attk_coord)
            shot_log.append(" HIT" if hit else " MISS")
            if sunk:
                shot_log.append(f" You sank my {ship}!")
                if defender.is_dead():
                    shot_log.append(" Game Over!")
                    winner = attacker
                    loser = defender
            turn_log.append(" :: ".join(shot_log))
            self.half_turn = 1 if self.half_turn == 0 else 0
            if winner:
                self.logs["turns"].append(turn_log)

        return (winner, loser)

    def set_boards(self) -> None:
        """Clear boards and place ships for both players."""
        for player in self.players:
            player.clear_boards()
            ship_log = place_ships(player)
            self.logs["debug"].append(ship_log)

    def show_log(self) -> None:
        """Print a pretty version of the game logs."""
        print(stringify(self.logs["turns"]))

    def _show_debug_logs(self) -> None:
        """Print the debug logs."""
        print(stringify(self.logs["debug"]))
