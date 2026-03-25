

class Enemy:
    def __init__(self, name, hp, attack, speed, armor, moves, xp_reward, gold_reward):
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
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward
        self.loot = []

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        reduced = round(damage * (100 / (100 + self.armor)))
        self.hp -= reduced
        return reduced

    def attack_player(self, player, log):
        player.take_damage(self.attack, self, log)

    def drop_loot(self):
        return self.loot

    def reset_combat_stats(self):
        self.attack = self.base_attack
        self.armor = self.base_armor
    