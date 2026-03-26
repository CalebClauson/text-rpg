import random

def apply_status(target, effect, log, tag="normal"):
    chance = effect.get("chance", 1.0)

    if random.random() > chance:
        log(f"{target.name} resisted {effect['effect']}!", tag)
        return False

    status_name = effect["effect"]
    duration = effect.get("duration", 1)

    # refresh existing status instead of stacking it
    for status in target.status_effects:
        if status["name"] == status_name:
            status["duration"] = duration
            if "value" in effect:
                status["value"] = effect["value"]
            log(f"{target.name}'s {status_name} was refreshed.", tag)
            return True

    new_status = {
        "name": status_name,
        "duration": duration
    }

    if "value" in effect:
        new_status["value"] = effect["value"]

    target.status_effects.append(new_status)

    if status_name == "poison":
        log(f"{target.name} was poisoned for {duration} turns!", tag)
    elif status_name == "stun":
        log(f"{target.name} was stunned!", tag)

    return True

def process_status_start_turn(target, log, tag="normal"):
    stunned = False

    for status in target.status_effects:
        if status["name"] == "poison":
            damage = status.get("value", 5)
            target.hp -= damage
            if target.hp < 0:
                target.hp = 0
            log(f"{target.name} takes {damage} poison damage!", tag)

        elif status["name"] == "stun":
            stunned = True
            log(f"{target.name} is stunned and cannot act!", tag)

    return stunned

def update_status_durations(target, log, tag="normal"):
    expired = []

    for status in target.status_effects:
        status["duration"] -= 1
        if status["duration"] <= 0:
            expired.append(status)

    for status in expired:
        target.status_effects.remove(status)
        log(f"{status['name'].capitalize()} wore off of {target.name}.", tag)