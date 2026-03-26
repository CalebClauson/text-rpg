from .enemy import Enemy
from player import Player
import json
import random
from .status_effects import apply_status, process_status_start_turn, update_status_durations

with open("assets/moves.json", "r") as f:
    MOVES = json.load(f)

WIDTH = 10


def generate_enemy(player):
    with open("assets/enemies.json", "r") as f:
        enemies_data = json.load(f)

    enemy_names = list(enemies_data.keys())
    weights = [enemies_data[name].get("weight", 1) for name in enemy_names]

    enemy_name = random.choices(enemy_names, weights=weights, k=1)[0]
    enemy_data = enemies_data[enemy_name]

    level_bonus = player.level - 1

    scaled_hp = enemy_data["hp"] + (level_bonus * 4)
    scaled_attack = enemy_data["attack"] + (level_bonus * 2)
    scaled_speed = enemy_data["speed"] + (level_bonus // 3)
    scaled_armor = enemy_data["armor"] + (level_bonus // 2)

    scaled_xp = enemy_data["xp_reward"] + (level_bonus * 3)
    scaled_gold = enemy_data["gold_reward"] + (level_bonus * 2)

    return Enemy(
        enemy_name.capitalize(),
        scaled_hp,
        scaled_attack,
        scaled_speed,
        scaled_armor,
        enemy_data["moves"],
        scaled_xp,
        scaled_gold
    )


def combat_encounter(player, log):
    enemy = generate_enemy(player)
    log(f"A {enemy.name} appears!")
    log("-" * WIDTH)

    if enemy.speed > player.speed:
        log(f"{enemy.name} outsped {player.name}.", "enemy")
        result = enemy_turn(player, enemy, log, tag="enemy")
        return enemy, result

    return enemy, "continue"


def get_move(move_id):
    return MOVES[move_id]


def handle_potion(player, enemy, log):
    player.use_item("potion", log)
    return "continue"


def handle_run(player, enemy, log):
    success = player.run(enemy, log)
    if success:
        return "escaped"
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
            log(f"{user.name} used {move['name']} and healed {heal_amount} HP.", tag)

        elif effect["type"] == "buff":
            stat_name = effect["stat"]
            buff_value = effect["value"]
            current_value = getattr(target, stat_name)
            setattr(target, stat_name, current_value + buff_value)
            log(f"{user.name}'s {stat_name} increased by {buff_value}.", tag)

        elif effect["type"] == "status":
            if effect["target"] == "enemy":
                apply_status(other, effect, log, tag)
            elif effect["target"] == "self":
                apply_status(user, effect, log, tag)

        elif effect["type"] == "drain":
            damage = round(user.attack * effect["multiplier"])
            actual_damage = target.take_damage(damage)
            heal_amount = round(actual_damage * effect["heal_percent"])
            user.hp = min(user.max_hp, user.hp + heal_amount)
            log(f"{user.name} used {move['name']}, dealt {actual_damage} damage, and healed {heal_amount} HP.", tag)

    if not other.is_alive():
        log(f"{other.name} has been defeated!")
        user.reset_combat_stats()
        other.reset_combat_stats()
        return "enemy_dead"

    if not user.is_alive():
        log(f"{user.name} has fallen.", tag)
        return "player_dead"

    return "continue"


def enemy_turn(player, enemy, log, tag="enemy"):
    user = enemy
    other = player

    stunned = process_status_start_turn(enemy, log, tag)

    if not enemy.is_alive():
        log(f"{enemy.name} has been defeated!")
        return "enemy_dead"

    if stunned:
        update_status_durations(enemy, log, tag)
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
        log(f"{enemy.name} has no moves!", tag)
        return "continue"

    result = handle_move(user, other, chosen_move, log, tag)

    if result in ["enemy_dead", "player_dead"]:
        return result

    update_status_durations(enemy, log, tag)
    return result


def process_victory(player, enemy, log):
    player.gold += enemy.gold_reward
    log(f"{player.name} gained {enemy.gold_reward} gold!")
    log(f"{player.name} gained {enemy.xp_reward} experience!")
    return player.gain_xp(enemy.xp_reward, log, "player")


def resolve_player_turn(player, enemy, action, log, move_id=None):
    stunned = process_status_start_turn(player, log, tag="player")

    if not player.is_alive():
        return "player_dead"

    if stunned:
        update_status_durations(player, log, tag="player")
        return enemy_turn(player, enemy, log, tag="enemy")

    if action == "attack":
        result = handle_move(player, enemy, move_id, log, "player")
    elif action == "heal":
        result = handle_potion(player, enemy, log)
    elif action == "run":
        result = handle_run(player, enemy, log)
    else:
        return "continue"

    update_status_durations(player, log, tag="player")

    if result in ["enemy_dead", "player_dead", "escaped"]:
        return result

    return enemy_turn(player, enemy, log, tag="enemy")