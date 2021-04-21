"""CPU Battleship Battle!!!

Usage:
_cpu_test.py $cpu1_level $cpu2_level $num_games
"""
import sys

from game import CPU, Battleship


def battle(cpu1_lvl: int, cpu2_lvl: int, num_games: int):
    """Battle them bots!"""
    if num_games < 0:
        sys.exit('Invalid number of games')
    cpu_1 = CPU(f'cpu1 lvl: {cpu1_lvl}', level=cpu1_lvl)
    cpu_2 = CPU(f'cpu2 lvl: {cpu2_lvl}', level=cpu2_lvl)

    played = 0
    while played < num_games:
        played += 1
        winner, loser = Battleship(cpu_1, cpu_2).play_game()
        winner.win()
        loser.lose()

    print(cpu_1, '--', cpu_2)


if __name__ == '__main__':
    args = sys.argv[1:]
    try:
        battle(int(args[0]), int(args[1]), int(args[2]))
    except IndexError:
        print(__doc__)
    except TypeError:
        print(__doc__)
