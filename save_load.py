import json
from player import Player

def load_player():
    try:
        with open("assets/player.json", "r") as f:
            data = json.load(f)

        player = Player(
            data["name"],
            data["hp"],
            data["attack"]
        )

        player.max_hp = data["max_hp"]
        player.inventory = data["inventory"]
        player.gold = data["gold"]

        return player

    except FileNotFoundError:
        # first time playing → create new player
        return Player("Hero", 100, 10)

def load_player():
    try:
        with open("assets/player.json", "r") as f:
            data = json.load(f)

        player = Player(
            data["name"],
            data["hp"],
            data["attack"]
        )

        player.max_hp = data["max_hp"]
        player.inventory = data["inventory"]
        player.gold = data["gold"]

        return player

    except FileNotFoundError:
        # first time playing → create new player
        return Player("Hero", 100, 10)