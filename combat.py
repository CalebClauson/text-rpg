from enemy import Enemy
import json
import random

WIDTH = 10


def generate_enemy():
    with open("assets/enemies.json", "r") as f:
        enemies_data = json.load(f)

    enemy_name = random.choice(list(enemies_data.keys()))
    enemy_data = enemies_data[enemy_name]

    return Enemy(
        enemy_name.capitalize(),
        enemy_data["hp"],
        enemy_data["attack"]
    )


def combat_encounter(log):
    enemy = generate_enemy()
    log(f"A {enemy.name} appears!")
    log("-" * WIDTH)
    log(f"{enemy.name} {enemy.hp}/{enemy.max_hp}")
    return enemy


def handle_attack(player, enemy, log):
    player.attack_enemy(enemy, log)

    if not enemy.is_alive():
        log(f"{enemy.name} has been defeated!")
        return "enemy_dead"

    enemy.attack_player(player, log)

    if not player.is_alive():
        log(f"{player.name} has fallen...")
        return "player_dead"

    return "continue"


def handle_heal(player, enemy, log):
    player.use_item("potion", log)

    if not enemy.is_alive():
        log(f"{enemy.name} has been defeated!")
        return "enemy_dead"

    enemy.attack_player(player, log)

    if not player.is_alive():
        log(f"{player.name} has fallen...")
        return "player_dead"

    return "continue"


def handle_run(player, enemy,log):
    success = player.run(enemy, log)

    if success:
        return "escaped"

    enemy.attack_player(player, log)

    if not player.is_alive():
        log(f"{player.name} has fallen...")
        return "player_dead"

    return "continue"