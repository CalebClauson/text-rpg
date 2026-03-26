import json
from player import Player
import os

def new_player(name):
    return Player(
        name,
        100,
        10,
        5,
        0,
        ["slash"],
        [],
        0,
        1,
        0,
        25
    )

def load_player():
    try:
        with open("assets/player.json", "r") as f:
            data = json.load(f)

        player = Player(
            data["name"],
            data["hp"],
            data["attack"],
            data.get("speed", 5),
            data.get("armor", 0),
            data.get("moves", ["slash"]),
            data.get("inventory", []),
            data.get("gold", 0),
            data.get("level", 1),
            data.get("xp", 0),
            data.get("xp_to_next", 25)
        )

        player.max_hp = data.get("max_hp", player.hp)

        return player

    except FileNotFoundError:
        return None

def save_player(player):
    data = {
        "name": player.name,
        "hp": player.hp,
        "max_hp": player.max_hp,
        "attack": player.base_attack,
        "speed": player.speed,
        "armor": player.base_armor,
        "moves": player.moves,
        "inventory": player.inventory,
        "gold": player.gold,
        "level": player.level,
        "xp": player.xp,
        "xp_to_next": player.xp_to_next
    }

    with open("assets/player.json", "w") as f:
        json.dump(data, f, indent=2)

def delete_player_save():
    if os.path.exists("assets/player.json"):
        os.remove("assets/player.json")