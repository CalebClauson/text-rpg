from enemy import Enemy
import json
import random
from status_effects import apply_status, process_status_start_turn, update_status_durations

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
        log(f"{enemy.name} outsped {player.name}....", "enemy")
        enemy_turn(player, enemy, log)
    return enemy

def get_move(move_id):
    return MOVES[move_id]

def handle_potion(player, enemy, log):
    player.use_item("potion", log)

    enemy.attack_player(player, log)

    if not player.is_alive():
        log(f"{player.name} has fallen...", "enemy")
        return "player_dead"

    return "continue"

def handle_run(player, enemy,log):
    success = player.run(enemy, log)

    if success:
        return "escaped"

    enemy_turn(player, enemy, log)

    if not player.is_alive():
        log(f"{player.name} has fallen...", "enemy")
        return "player_dead"

    return "continue"

def handle_move(user, other, move_id, log, tag="normal"):
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
            log(f"{user.name} used {move['name']} and dealt {actual_damage} damage to {target.name}.", tag)

        elif effect["type"] == "heal":
            heal_amount = effect["value"]
            target.hp = min(target.max_hp, target.hp + heal_amount)
            log(f"{user.name} used {move['name']} and healed {heal_amount} HP.")

        elif effect["type"] == "buff":
            stat_name = effect["stat"]
            buff_value = effect["value"]

            current_value = getattr(target, stat_name)
            setattr(target, stat_name, current_value + buff_value)

            log(f"{user.name}'s {stat_name} increased by {buff_value}.")

        elif effect["type"] == "status":
            if effect["target"] == "enemy":
                apply_status(other, effect, log)
            elif effect["target"] == "self":
                apply_status(user, effect, log)

        elif effect["type"] == "drain":
            damage = round(user.attack * effect["multiplier"])
            actual_damage = target.take_damage(damage)

            heal_amount = round(actual_damage * effect["heal_percent"])
            user.hp = min(user.max_hp, user.hp + heal_amount)

            log(f"{user.name} used {move['name']}, dealt {actual_damage} damage, and healed {heal_amount} HP.")


    if not other.is_alive():
        log(f"{other.name} has been defeated!")

        if hasattr(other, "xp_reward") and hasattr(other, "gold_reward"):
            user.gain_xp(other.xp_reward, log)
            user.gold += other.gold_reward
            log(f"{user.name} gained {other.gold_reward} gold!")
            log(f"{user.name} gained {other.xp_reward} experience!")

        user.reset_combat_stats()
        other.reset_combat_stats()
        return "enemy_dead"

    if not user.is_alive():
        log(f"{user.name} has fallen...")
        return "player_dead"
    

    return "continue"
        
def enemy_turn(player, enemy, log):
    user = enemy
    other = player

    stunned = process_status_start_turn(enemy, log)

    if not enemy.is_alive():
        log(f"{enemy.name} has been defeated!")
        return "enemy_dead"

    if stunned:
        update_status_durations(enemy, log)
        return "enemy_skipped"

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

    result = handle_move(user, other, chosen_move, log, "enemy")

    if result in ["enemy_dead", "player_dead"]:
        return result

    update_status_durations(enemy, log)
    return result