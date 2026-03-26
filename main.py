from systems.enemy import Enemy
from gui import start_gui
from save_load import load_player


def main():
    player = load_player()
    enemy = None
    start_gui(player, enemy)


main()