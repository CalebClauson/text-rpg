import json
import random

from enemy import Enemy
from gui import start_gui
from save_load import load_player
from combat import *


def main():
    player = load_player()
    enemy = None
    start_gui(player, enemy)


main()