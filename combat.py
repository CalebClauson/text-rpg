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
        enemy_data["attack"],
        enemy_data["xp_reward"],
        enemy_data["gold_reward"]
    )


def combat_encounter(log):
    enemy = generate_enemy()
    log(f"A {enemy.name} appears!")
    log("-" * WIDTH)
    log(f"{enemy.name} {enemy.hp}/{enemy.max_hp}")
    return enemy


def handle_attack(player, enemy, move, log):
    damage = round(player.attack * move["multiplier"])
    enemy.take_damage(damage)
    log(f"{player.name} used {move['name']} and dealt {damage} damage!")
    if enemy.hp < 0:
        log(f"{enemy.name} HP: 0/{enemy.max_hp}")
    else:
        log(f"{enemy.name} HP: {enemy.hp}/{enemy.max_hp}")

    if not enemy.is_alive():
        log(f"{enemy.name} has been defeated!")

        player.gain_xp(enemy.xp_reward, log)
        player.gold += enemy.gold_reward
        log(f"{player.name} gained {enemy.gold_reward} gold!")

        return "enemy_dead"

    enemy.attack_player(player, log)

    if not player.is_alive():
        log(f"{player.name} has fallen...")
        return "player_dead"

    return "continue"

def handle_move(player, enemy, log):
    damage = player.attack * player.move["multiplier"]
    log(f"{player.name} used {player.move['name']}!")
    enemy.take_damage(damage)


def handle_heal(player, enemy, log):
    player.use_item("potion", log)

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