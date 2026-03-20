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


def combat(player, enemy):
    turn = 0

    while player.is_alive() and enemy.is_alive():
        if turn % 2 == 0:
            turn += 1
        else:
            enemy.attack_player(player)
            turn += 1

    if player.is_alive():
        print(f"{enemy.name} has been defeated!")
    else:
        print(f"{player.name} has fallen...")

def combat_encounter(log):
    enemy = generate_enemy()
    log(f"A {enemy.name} appears!")
    log(f"-" * WIDTH)
    log(f"{enemy.name} {enemy.hp}/{enemy.max_hp}")
    return enemy