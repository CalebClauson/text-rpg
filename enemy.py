

class Enemy:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack

        #loot drop logic
        self.loot = []

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, player):
        self.hp -= player.attack

    def attack_player(self, player):
        player.hp -= self.attack

    def drop_loot(self):
        return self.loot


    