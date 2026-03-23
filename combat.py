from enemy import Enemy
import json
import random
import time

with open("assets/moves.json", "r") as f:
    MOVES = json.load(f)

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
        enemy_data["armor"],
        enemy_data["moves"],
        enemy_data["xp_reward"],
        enemy_data["gold_reward"]
    )

def combat_encounter(log):
    enemy = generate_enemy()
    log(f"A {enemy.name} appears!")
    log("-" * WIDTH)
    log(f"{enemy.name} {enemy.hp}/{enemy.max_hp}")
    return enemy

def get_move(move_id):
    return MOVES[move_id]

def enemy_turn(player, enemy, log):
    attack_moves = []
    other_moves = []

    for move_id in enemy.moves:
        move = get_move(move_id)

        if move["type"] == "damage":
            attack_moves.append(move)
        else:
            other_moves.append(move)

    if not attack_moves:
        log(f"{enemy.name} hesitated...")
        return "continue"
    
    move = random.choice(attack_moves)
    damage = round(enemy.attack * move["multiplier"])
    player.take_damage(damage, enemy, log)
    log(f"{enemy.name} used {move['name']} and dealt {damage} damage!")

    if not player.is_alive():
        log(f"{player.name} has fallen...")
        return "player_dead"

    return "continue"


def player_turn(player, enemy, move_id, log):
    move = get_move(move_id)

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

def handle_potion(player, enemy, log):
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