import items, world
import random

class Player():
    """ A super class for all player types """
    def __init__(self):
        self.hp = 100
        self.maxhp = 200
        self.speed = 10
        self.inventory = {
                            "Gold": items.Gold(50),
                            "Weapons": [items.Dagger()]
                        }
        self.location_x, self.location_y = world.starting_position
        self.victory = False
    
    def isAlive(self):
        return self.hp > 0
    
    def inventorySummary(self):
        print("\n\n\t*** PLAYER INVENTORY ***")
        print("   Gold stash : {}".format(self.inventory["Gold"].balance()))
        print("   Weapon stash :")
        for w in self.inventory["Weapons"]:
            print("\t\t",w)
        print("\n\n")
    
    def statSummary(self):
        print("\n\n\t*** PLAYER STATS ***")
        print("\t    HP : {}".format(self.hp))
        print("\t    Speed : {}\n\n".format(self.speed))
    
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
        for i in self.inventory["Weapons"]:
            if isinstance(i, items.Weapon): # should be so becuase of the dictionary but still checking.
                if i.damage > maxDmg:
                    maxDmg = i.damage
                    bestWeapon = i
        print("\n You use {} to deal {} damage to the {}".format(bestWeapon.name,maxDmg, enemy.name))
        enemy.hp -= maxDmg
        if not enemy.isAlive():
            print(" You killed the {}\n".format(enemy.name))
        else:
            print(" Remaining HP of the {} is {}\n".format(enemy.name, enemy.hp))
    
    def flee(self, tile):
        #Relocate to random location.
        available_moves = tile.available_moves()
        r = random.randint(0, len(available_moves) - 1)
        deduction = int(0.1 * self.inventory["Gold"].balance())
        print("\n\n\t*** You ran for your life without looking back. You dropped {} coins while fleeing. ***".format(deduction))
        self.inventory["Gold"].removeGold(deduction)
        print("\t*** You have {} gold remaining in your pouch. ***\n\n".format(self.inventory["Gold"].balance()))

        self.do_action(available_moves[r])

    def do_action(self, action, **kwargs):
        action_method = getattr(self, action.method.__name__)
        if action_method:
            action_method(**kwargs)

    def __str__(self):
        return "\nI have {} health and {} speed. I am at position ({},{}) and i have the following items in my inventory: {}\n".format(self.hp, self.speed, self.location_x, self.location_y, self.inventorySummary)