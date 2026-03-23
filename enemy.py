

class Enemy:
    def __init__(self, name, hp, attack, armor,  moves, xp_reward, gold_reward):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.armor = armor
        self.moves = moves
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward
        self.loot = []

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= round(damage * (100/(100 + self.armor)))

    def attack_player(self, player, log):
        player.take_damage(self.attack, self, log)

    def drop_loot(self):
        return self.loot


    