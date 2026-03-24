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
        enemy_data["speed"],
        enemy_data["armor"],
        enemy_data["moves"],
        enemy_data["xp_reward"],
        enemy_data["gold_reward"]
    )

def combat_encounter(player, log):
    enemy = generate_enemy()
    log(f"A {enemy.name} appears!")
    log("-" * WIDTH)
    if enemy.speed > player.speed:
        log(f"{enemy.name} outsped {player.name}....")
        enemy_turn(player, enemy, log)
    return enemy

def get_move(move_id):
    return MOVES[move_id]

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

    enemy_turn(player, enemy, log)

    if not player.is_alive():
        log(f"{player.name} has fallen...")
        return "player_dead"

    return "continue"

def handle_move(user, other, move_id, log):
    move = get_move(move_id)

    if not move:
        log(f"Move '{move_id}' was not found.")
        return "continue"

    for effect in move["effects"]:
        if effect["target"] == "self":
            target = user
        elif effect["target"] == "enemy":
            target = other
        else:
            log(f"{move['name']} has an invalid target.")
            return "continue"

        if effect["type"] == "damage":
            damage = round(user.attack * effect["multiplier"])
            actual_damage = target.take_damage(damage)
            log(f"{user.name} used {move['name']} and dealt {actual_damage} damage to {target.name}.")

        elif effect["type"] == "heal":
            heal_amount = effect["value"]
            target.hp = min(target.max_hp, target.hp + heal_amount)
            log(f"{user.name} used {move['name']} and healed {heal_amount} HP.")

        elif effect["type"] == "buff":
            log(f"{user.name} used {move['name']} and gained +{effect['value']} {effect['stat']} for {effect['duration']} turns.")

        elif effect["type"] == "status":
            log(f"{user.name} used {move['name']} and tried to apply {effect['effect']} to {target.name}.")

        elif effect["type"] == "drain":
            damage = round(user.attack * effect["multiplier"])
            target.take_damage(damage)

            heal_amount = round(damage * effect["heal_percent"])
            user.hp = min(user.max_hp, user.hp + heal_amount)

            log(f"{user.name} used {move['name']}, dealt {damage} damage, and healed {heal_amount} HP.")

    if not other.is_alive():
        log(f"{other.name} has been defeated!")

        if hasattr(other, "xp_reward") and hasattr(other, "gold_reward"):
            user.gain_xp(other.xp_reward, log)
            user.gold += other.gold_reward
            log(f"{user.name} gained {other.gold_reward} gold!")
            log(f"{user.name} gained {other.xp_reward} experience!")
            return "enemy_dead"

        return "player_dead"

    if not user.is_alive():
        log(f"{user.name} has fallen...")
        return "player_dead"
    

    return "continue"
        
def enemy_turn(player, enemy, log):
    user = enemy
    other = player

    attack_moves = []
    heal_moves = []
    other_moves = []

    for move_id in enemy.moves:
        move = get_move(move_id)

        if not move:
            continue

        effect_types = [effect["type"] for effect in move["effects"]]

        if "heal" in effect_types:
            heal_moves.append(move_id)
        elif "damage" in effect_types or "drain" in effect_types:
            attack_moves.append(move_id)
        else:
            other_moves.append(move_id)

    if enemy.hp <= enemy.max_hp * 0.4 and heal_moves:
        chosen_move = random.choice(heal_moves)
    elif attack_moves:
        chosen_move = random.choice(attack_moves)
    elif other_moves:
        chosen_move = random.choice(other_moves)
    else:
        log(f"{enemy.name} has no moves!")
        return "continue"

    return handle_move(user, other, chosen_move, log)