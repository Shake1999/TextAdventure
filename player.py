import items, world

class Player():
    """ A super class for all player types """
    def __init__(self):
        self.hp = 100
        self.maxhp = 200
        self.speed = 10
        self.inventory = [items.Gold(50), items.Dagger()]
        self.location_x, self.location_y = world.starting_position
        self.victory = False
    
    def isAlive(self):
        return self.hp > 0
    
    def inventorySummary(self):
        print("******* PLAYER INVENTORY *******")
        for item in self.inventory:
            print(item)
    
    def move(self, dx, dy):
        self.location_x += dx
        self.location_y += dy
        print(world.tile_exists(self.location_x, self.location_y).introduction())
    
    def moveNorth(self):
        self.move(0,-1)
    def moveSouth(self):
        self.move(0,1)
    def moveEast(self):
        self.move(1,0)
    def moveWest(self):
        self.move(-1,0)
    
    def attack(self, enemy):
        bestWeapon = None
        maxDmg = 0
        for i in self.inventory:
            if isinstance(i, items.Weapon):
                if i.damage > maxDmg:
                    maxDmg = i.damage
                    bestWeapon = i
        print(" You use {} to deal {} damage to {}".format(i.name,maxDmg, enemy.name))
        enemy.hp -= maxDmg
        if not enemy.isAlive():
            print("You killed the {}".format(enemy.name))
        else:
            print(" Remaining HP of the {} is {}".format(enemy.name, enemy.hp))
    
    def do_action(self, action, **kwargs):
        action_method = getattr(self, action.method.__name__)
        if action_method:
            action_method(**kwargs)

    def __str__(self):
        return "I have {} health and {} speed. I am at position ({},{}) and i have the following items in my inventory: \n".format(self.hp, self.speed, self.location_x, self.location_y,self.inventorySummary)