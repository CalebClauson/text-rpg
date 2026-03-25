import random
import json

with open("assets/items.json", "r") as f:
    ITEMS = json.load(f)

class Player:
    def __init__(self, name, hp, attack, speed, armor, moves, inventory, gold, level, xp, xp_to_next):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.base_attack = attack
        self.speed = speed
        self.armor = armor
        self.base_armor = armor
        self.status_effects = []
        self.moves = moves
        self.inventory = inventory if inventory is not None else []
        self.gold = gold
        self.level = level
        self.xp = xp
        self.xp_to_next = xp_to_next

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        reduced = round(damage * (100 / (100 + self.armor)))
        self.hp -= reduced
        return reduced

    def use_item(self, item_id, log):
         if item_id not in self.inventory:
            log("You do not have that item.")
            return

         item = ITEMS[item_id]

         if item["type"] == "heal":
             self.hp += item["value"]

             if self.hp > self.max_hp:
                 self.hp = self.max_hp

             log(f"You used {item['name']} and healed {item['value']} HP!")
             self.inventory.remove(item_id)

    def run(self, enemy, log):
        chance = random.choice(["Success", "Fail"])
        if chance == "Success":
            log("You managed to scrape away...")
            return True
        else:
            log(f"{self.name} stumbled and {enemy.name} caught you...")
            return False

    def backpack(self, log):
        if not self.inventory:
            log("Your backpack is empty.")
            return

        log("Backpack:")

        item_counts = {}

        for item_id in self.inventory:
            item_counts[item_id] = item_counts.get(item_id, 0) + 1

        for item_id, count in item_counts.items():
            item = ITEMS[item_id]
            log(f"- {item['name']} x{count}")

    def gain_xp(self, amount, log , tag="player"):
        self.xp += amount
        if self.xp >= self.xp_to_next:
            self.level += 1
            log(f"{self.name} has leveled up! Level {self.level}" ,tag)
            self.base_attack += 2
            self.attack = self.base_attack
            self.max_hp += 10
            self.hp = self.max_hp
            self.xp_to_next = self.xp_to_next + (self.level * 10)
            self.xp = 0

    def show_stats(self, log):
        log(f"Name: {self.name}")
        log(f"Health: {self.hp}/{self.max_hp}")
        log(f"Attack: {self.attack}")
        log(f"Gold: {self.gold}")

    def reset_combat_stats(self):
        self.attack = self.base_attack
        self.armor = self.base_armor