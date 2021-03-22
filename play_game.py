import os
import sys

from battleship import Ship, Player, CPU


BANNER = """
*******************************
****** BATTLESHIP v1.0.0 ******
*******************************
"""

SHIPS = {
    "Carrier": 5,
    "Battleship": 4,
    "Submarine": 3,
    "Destroyer": 3,
    "Patrol Boat": 2
}

def welcome() -> str:
    """The welcome screen at beginning of game where user enters their name and
    the player and cpu instances are created.  Then calls function `play` to
    continue with the game.
    """
    os.system('clear')
    print(BANNER)
    name = input('Enter Name: ')
    player = Player(name)
    cpu = CPU('CPU')

    return play(player, cpu)

def play(player: Player, cpu: CPU) -> str:
    """The meat of the module for playing the game.  The first option is whether
    to continue playing or quit.  If player chooses to continue, then the boards
    are reset and ships are placed.  The game is then played with turns alternating
    between the player and cpu.  The game is ended when either players' ships
    have all been destroyed.

    Parameters
    ----------
    player : class <`battleship.Player`> instance.
        The human player.
    cpu : class <`battleship.CPU`> instance.
        The CPU player.
    """
    while True:
        os.system('clear')
        print(player)
        print(player.stats())
        print(cpu)
        print(cpu.stats())
        cont = input('Play a game? 1-yes  2-no: ')
        if cont == '2':
            return 'See you next time!'
        elif cont == '1':
            break
    
    # Reset Boards
    player.clear_boards()
    cpu.clear_boards()

    # Place ships
    cpu.add_all_ships()
    for ship_name, ship_size in SHIPS.items():
        built = False
        while not built:
            os.system('clear')
            print(f'*** Building {ship_name} ***')
            player.show_ship_board()
            print(f'Ship Length: {ship_size}')
            bow = input('Bow Coordinate: ').upper()
            heading = input('Direction: ').capitalize()
            try:
                if player.add_ship(Ship.build(ship_name, bow, heading)):
                    built = True
            except Exception as err:
                print(err)

    # Play the game
    winner = None
    loser = None
    while not winner:
        os.system('clear')
        # Player's Turn
        while True:
            os.system('clear')
            print(f"{player.name}'s Turn:")
            player.show_attack_board()
            attk_coord = input('Choose coordinate to attack (`q` to quit): ').upper()
            if 'Q' in attk_coord:
                return('Player quit...')
            if not player.attack_board.is_attacked(attk_coord):
                break
        os.system('clear')
        reply = cpu.get_rekt(attk_coord)
        hit = "HIT" in reply
        player.add_attack_peg(attk_coord, hit)
        print(f"{player.name} attacks {attk_coord}:")
        player.show_attack_board()
        input(reply)
        if cpu.is_dead():
            winner = player
            loser = cpu
            break

        # CPU's turn
        os.system('clear')
        attk_coord = cpu.choose_attack_coordinate()
        reply = player.get_rekt(attk_coord)
        hit = "HIT" in reply
        cpu.add_attack_peg(attk_coord, hit)
        print(f'CPU attacks {attk_coord}...')
        player.show_ship_board()
        input(reply)
        if player.is_dead():
            winner = cpu
            loser = player
            break

    # We've got a WINNER!!!!
    os.system('clear')
    print(f'Congrats {winner.name}!!!')
    print(f'\nPlayer Board:\n')
    player.show_ship_board()
    print(f'\n\nCPU Board:\n')
    cpu.show_ship_board()
    input(f'\nEnter to continue...')
    
    winner.win()
    loser.lose()
    play(player, cpu)

if __name__ == '__main__':
    sys.exit(welcome())
