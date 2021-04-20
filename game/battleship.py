"""Module which contains the game.

Rules of the game:
https://www.hasbro.com/common/instruct/Battleship.PDF


"""

import os
from typing import Tuple

from game.player import Human, Player


class GameLog:
    """Class to track the logs from the Battleship game."""

    def __init__(self) -> None:
        self.log = []
        self.debug_log = []

    def __len__(self) -> int:
        return len(self.log)

    def add(self, turn_num: int, log: str) -> None:
        """Add log entry."""
        if len(self) < turn_num:
            self.log.append([])
        self.log[turn_num - 1].append(log)

    def debug(self, log: str) -> None:
        """Add a debug log entry."""
        self.debug_log.append(log)

    def show(self) -> None:
        """Print the game logs."""
        max_l = 0
        for log in self.log:
            if len(log[0]) > max_l:
                max_l = len(log[0])

        for _i, log in enumerate(self.log):
            turn = _i + 1
            t_space = '  ' if turn < 10 else ' '

            l_space = (max_l - len(log[0]) + 1) * ' '
            log = f'{l_space}'.join(log)
            print(f"{turn}.{t_space}{log}")

    def show_debug(self) -> None:
        """Print the debug logs."""
        for log in self.debug_log:
            print(log)


GameResult = Tuple[Player, Player]


class Battleship:
    """A game of Battleship."""

    def __init__(self, player1: Player, player2: Player) -> None:
        self.players = [player1, player2]
        self.log = GameLog()

        self.set_boards()

    def __len__(self) -> int:
        return len(self.log)

    def play_game(self) -> GameResult:
        """Manage the gameplay.

        Returns
        -------
        result : GameResult
            (winner, loser)
        """
        half_turns = 0
        winner = None
        loser = None
        output = "Let's Play!!!"
        while winner is None:
            turn_num = int(half_turns / 2) + 1
            if turn_num > 100:
                # break if somehow we get to a full board with no winner.
                self.log.add(turn_num, 'Q!!')
                break
            attacker = self.players[half_turns % 2]
            defender = self.players[half_turns % 2 - 1]

            # display board if human is playing.
            if isinstance(attacker, Human):
                os.system('clear')
                print(output)
                attacker.show_boards()

            attk_coord = attacker.choose("attack_coordinate")
            if 'Q' in attk_coord:
                winner = defender
                loser = attacker
                self.log.add(turn_num, 'Q**')
                continue
            if not attacker.attack_board.unattacked(attk_coord):
                continue
            result = defender.attacked(attk_coord)
            defender.add_ship_peg(attk_coord, result)
            attacker.add_attack_peg(attk_coord, result)
            hit, sunk, ship = result
            shot_log = attk_coord
            output = f'{attacker.name} attacks {attk_coord}: '
            if hit:
                output += 'HIT: '
                if sunk:
                    shot_log += ship.symbol()
                    output += f'You Sank My {ship.name}!'
                    if defender.is_dead():
                        shot_log += "**"
                        winner = attacker
                        loser = defender
                else:
                    shot_log += ship.symbol().lower()
            else:
                output += ' MISS!'

            self.log.add(turn_num, shot_log)
            half_turns += 1

        return (winner, loser)

    def set_boards(self) -> None:
        """Clear boards and place ships for both players."""
        for player in self.players:
            player.clear_boards()
            self.place_ships(player)

    def show_log(self) -> None:
        """Print a pretty version of the game logs."""
        self.log.show()

    def _show_debug_logs(self) -> None:
        """Print the debug logs."""
        self.log.show_debug()

    def place_ships(self, player: Player) -> None:
        """Guide player in placing ships on board."""
        for ship in player.ship_board.ships:
            built = False
            while not built:
                if isinstance(player, Human):
                    os.system('clear')
                    print(f'*** Building {ship} ***')
                    player.show_ship_board()
                    print(f'Ship Length: {len(ship)}')
                bow = player.choose("coordinate").upper()
                direction = player.choose("direction").upper()
                try:
                    built = player.add_ship(ship, bow, direction)
                except ValueError as err:
                    self.log.debug(f'Unable to add ship: {err}')
