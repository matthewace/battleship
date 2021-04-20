from game import CPU, Battleship

cpu_1 = CPU('cpu_1')
cpu_2 = CPU('cpu_2', level=1)


GAMES_PLAYED = 0
MAX_GAMES = 1000
while GAMES_PLAYED < MAX_GAMES:
    GAMES_PLAYED += 1
    winner, loser = Battleship(cpu_1, cpu_2).play_game()
    winner.win()
    loser.lose()

print(cpu_1, cpu_2)
