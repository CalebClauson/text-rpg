import random
import json

with open("assets/items.json", "r") as f:
    ITEMS = json.load(f)

class Player:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.inventory = []
        self.gold = 0

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage, enemy, log):
        self.hp -= damage
        log(f"You took {damage} damage from {enemy.name}!")
        log(f"{self.name} HP: {self.hp}/{self.max_hp}")

    def attack_enemy(self, enemy, log):
        if enemy.hp > 0:
            enemy.hp -= self.attack
            log(f"You dealt {self.attack} damage to {enemy.name}!")
            log(f"{enemy.name} {enemy.hp}/{enemy.max_hp}")
        else:
            log(f"{self.name} slaughtered the {enemy.name}")

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

    def run(self, enemy, combat, log):
        if combat:
            chance = random.choice(["Success", "Fail"])
            if chance == "Success":
                log("You managed to scrape away...")
                in_combat = False
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

    def show_stats(self, log):
        log(f"Name: {self.name}")
        log(f"Health: {self.hp}/{self.max_hp}")
        log(f"Attack: {self.attack}")
        log(f"Gold: {self.gold}")