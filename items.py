class Item():
    """ The base class for all items """
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value
    
    def __str__(self):
        return "Item name is {} and item value is {}.".format(self.name,self.value)

class Gold(Item):
    def __init__(self, amount):
        self.amount = amount
        super().__init__("Gold","InGame Currency to buy equipments for your hero", amount)
    def balance(self):
        return self.amount
    def addGold(self, amount):
        self.amount += amount
    def removeGold(self, amount):
        self.amount -= amount
    def __str__(self):
        return "{} gold coins".format(self.amount)

class Weapon(Item):
    """ Weapons for player """
    def __init__(self, name, desc, val, damage):
        self.damage = damage
        super().__init__(name, desc, val)
    def __str__(self):
        return "A {} which deals {} damage in one go.".format(self.name, self.damage)

class Sword(Weapon):
    """ The prophesized sword said to bring an end to evil """
    def __init__(self, dmg, val):
        super().__init__("Sword", "The prophesized sword said to bring an end to evil", val, dmg)

class MagicWand(Weapon):
    """ A skilled wizzard only needs his wand to destroy all his enemies """
    def __init__(self, dmg, val):
        super().__init__("Magic Wand", "An ancient wooden wand for skilled wizzards only", val, dmg)

class Dagger(Weapon):
    """ A small dagger which has gone blunt over the years """
    def __init__(self):
        super().__init__("Dagger", "A small dagger which has gone blunt over the years", 20, 15)

class Medicine(Item):
    def __init__(self, healValue, val):
        self.healing = healValue
        super().__init__("Medicine","A healing potion which restores some HP", val)
    def __str__(self):
        return " A Unique herbal medicine which restores {} HP.".format(self.healing)
