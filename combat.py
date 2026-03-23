from enemy import Enemy
import json
import random
import time

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

def enemy_turn(player, enemy, log):
    log("-" * WIDTH)
    log(f"{enemy.name} attacked {player.name} for {enemy.attack}")
    enemy.attack_player(player, log)

    if not player.is_alive():
        log(f"{player.name} has fallen...")
        log("-" * WIDTH)
        return "player_dead"

    log("-" * WIDTH)
    return "continue"

def handle_attack(player, enemy, move, log):
    #needs logic: potential elemtents
    if move["type"] == "damage":
        damage = round(player.attack * move["multiplier"])
        enemy.take_damage(damage)
        log(f"{player.name} used {move['name']} and dealt {damage} damage!")
        log(f"{enemy.name} HP: {max(enemy.hp, 0)}/{enemy.max_hp}")

        if enemy.hp <= 0:
            log(f"{enemy.name} has been defeated!")
            player.gain_xp(enemy.xp_reward, log)
            player.gold += enemy.gold_reward
            log(f"{player.name} gained {enemy.gold_reward} gold!")
            log(f"{player.name} gained {enemy.xp_reward} experience!")
            return "enemy_dead"

        return enemy_turn(player, enemy, log)

    #needs logic for potential mana to prevent infinite heals
    elif move["type"] == "heal":
        player.hp += move["value"]
        if player.hp > player.max_hp:
            player.hp = player.max_hp

        log(f"{player.name} used {move['name']} and healed {move['value']} HP!")
        return enemy_turn(player, enemy, log)

    #needs logic
    elif move["type"] == "buff":
        log(f"{player.name} used {move['name']} and gained +{move['value']} {move['stat']}!")
        return enemy_turn(player, enemy, log)

    #needs logic
    elif move["type"] == "status":
        log(f"{player.name} used {move['name']} and tried to apply {move['effect']}!")
        return enemy_turn(player, enemy, log)

    return "continue"

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