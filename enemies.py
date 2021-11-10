class Enemy():
    """ A super class for all enemy types """
    def __init__(self, name, hp, damage, speed):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.speed = speed
    
    def isAlive(self):
        return self.hp > 0
    
    def __str__(self):
        return "I am a {}. My health is {} and I deal {} damage at {} speed.".format(self.name, self.hp, self.damage, self.speed)

class Gargoyle(Enemy):
    """ A terrifying ancient enemy. Slow speed but high damage and large health pool """
    def __init__(self):
        super().__init__("Gargoyle", 100, 40,2)

class HungryRat(Enemy):
    """ A quick and tiny animal with sharp teeth spreading terror and disease """
    def __init__(self):
        super().__init__("Hungry Rat", 10, 2, 20)

class DemonicPriest(Enemy):
    """ A dark priest who worships Lucifer and needs sacrifices for endless rituals """
    def __init__(self):
        super().__init__("Demonic Priest", 80, 30, 4)

class SilverDragon(Enemy):
    """ The infamous silver dragon """
    def __init__(self):
        super().__init__("Silver Dragon", 150, 60, 20)
