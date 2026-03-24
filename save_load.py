import json
from player import Player

def load_player():
    try:
        with open("assets/player.json", "r") as f:
            data = json.load(f)

        player = Player(
            data["name"],
            data["hp"],
            data["attack"],
            data["speed"],
            data["armor"],
            data["moves"],
            data["inventory"],
            data["gold"],
            data["level"],
            data["xp"],
            data["xp_to_next"]
        )

        player.max_hp = data["max_hp"]

        return player

    except FileNotFoundError:
        return Player(
            "Hero",
            100,
            10,
            [],
            [],
            0,
            1,
            0,
            25
        )

def save_player(player):
    data = {
        "name": player.name,
        "hp": player.hp,
        "max_hp": player.max_hp,
        "attack": player.attack,
        "speed": player.speed,
        "armor": player.armor,
        "moves": player.moves,
        "inventory": player.inventory,
        "gold": player.gold,
        "level": player.level,
        "xp": player.xp,
        "xp_to_next": player.xp_to_next
    }

    with open("assets/player.json", "w") as f:
        json.dump(data, f, indent=2)