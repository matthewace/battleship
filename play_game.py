"""Play a game of Battleship."""

from __future__ import annotations

import os
import sys

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

"""


def welcome() -> str:
    """Get game type and player name (if human is playing)."""
    os.system('clear')
    print(BANNER)
    game_type = input('(P)lay or (S)im? ').upper()
    if game_type == 'P':
        p1_name = input('Player Name: ')
        player1 = Human(p1_name)
    else:
        player1 = CPU('cpu_p1')
    player2 = CPU('cpu_p2', level=3)

    play(player1, player2)


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


if __name__ == '__main__':
    sys.exit(welcome())
