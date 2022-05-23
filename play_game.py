"""Play a game of Battleship."""

from __future__ import annotations

import os
import sys

from datetime import datetime

from game import CPU, Human, Player, Battleship


BANNER = """
*******************************
****** BATTLESHIP v1.0.0 ******
*******************************
""".strip()

POSTGAME_OPTIONS = """
1: View Game Log
2: View Final Ship Boards
3: Continue

>>
"""


def _get_num_games() -> int:
    """Get number of simulated games to play."""
    num_games = -1
    print('How many games to simulate? (1 - 999)')
    while num_games not in range(1, 1000):
        num_games = input('>> ')
        if num_games.isnumeric():
            num_games = int(num_games)
    return num_games


def _get_cpu_level(cpu_name: str) -> int:
    """Ask user what level difficulty for CPU player."""
    cpu_level = -1
    print(f'Choose difficulty level for {cpu_name}')
    print('Dunce: 0 | Easy: 1 | Medium: 2 | Hard: 3')
    while cpu_level not in range(4):
        cpu_level = input('>> ')
        if cpu_level.isnumeric():
            cpu_level = int(cpu_level)
    return cpu_level


def welcome() -> str:
    """Get game type and player name (if human is playing)."""
    os.system('clear')
    print(BANNER)
    game_type = input('(P)lay or (S)im? ').upper()
    if game_type == 'P':
        p1_name = input('Player Name: ')
        player1 = Human(p1_name)
        lvl = _get_cpu_level('cpu_p2')
        player2 = CPU('cpu_p2', level=lvl)
        play(player1, player2)
    elif game_type == 'S':
        p1_lvl = _get_cpu_level('cpu_p1')
        p2_lvl = _get_cpu_level('cpu_p2')
        battle(p1_lvl, p2_lvl, num_games=_get_num_games())
    else:
        welcome()


def play(player1: Player, player2: Player) -> None:
    """Manage the game sessions.

    Parameters
    ----------
    player1 : class <`battleship.Player`> instance.
        The human player.
    player2 : class <`battleship.Player`> instance.
        The CPU player.
    """
    while True:
        # Provide option to play another game
        os.system('clear')
        print(player1)
        print(player2)
        cont = input('Play a game? 1-yes  2-no: ')
        if cont != '1':
            break

        # Play the game
        game = Battleship(player1, player2)
        winner, loser = game.play_game()

        # Post game
        winner.win()
        loser.lose()
        while True:
            os.system('clear')
            print(f"{winner.name} wins on turn {len(game)}!")
            next_step = input(POSTGAME_OPTIONS)
            if next_step == '1':
                os.system('clear')
                game.show_log()
                input('Enter to continue...')
            elif next_step == '2':
                os.system('clear')
                print("Winning Board:")
                winner.show_ship_board()
                print("\nLosing Board:")
                loser.show_ship_board()
                input('Enter to continue...')
            elif next_step == '3':
                break


def battle(cpu1_lvl: int, cpu2_lvl: int, num_games: int):
    """Battle them bots!"""
    if num_games < 0:
        sys.exit('Invalid number of games')
    cpu_1 = CPU(f'cpu1 lvl: {cpu1_lvl}', level=cpu1_lvl)
    cpu_2 = CPU(f'cpu2 lvl: {cpu2_lvl}', level=cpu2_lvl)

    played = 0
    total_turns = 0
    total_runtime = 0
    print(f'Simulating {num_games} games...')
    while played < num_games:
        played += 1
        start = datetime.now()
        game = Battleship(cpu_1, cpu_2)
        winner, loser = game.play_game()
        runtime = datetime.now() - start
        winner.win()
        loser.lose()
        total_turns += len(game.log)
        total_runtime += runtime.total_seconds()

    avg_turns = total_turns / num_games
    avg_runtime = total_runtime / num_games
    print(cpu_1, '--', cpu_2)
    print(f'avg_turns: {avg_turns} - avg_runtime: {avg_runtime}')


if __name__ == '__main__':
    sys.exit(welcome())
