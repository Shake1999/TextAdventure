import items, world
import random

class Player():
    """ A super class for all player types """
    def __init__(self):
        self.hp = 100
        self.speed = 10
        self.inventory = {
                            "Gold": items.Gold(50),
                            "Weapons": [items.Dagger()],
                            "Medicine": [items.Medicine(20, 100), items.Medicine(5, 50)]
                        }
        self.location_x, self.location_y = world.starting_position
        self.victory = False
    
    def isAlive(self):
        return self.hp > 0
    
    def inventorySummary(self):
        print("\n\n\t*** PLAYER INVENTORY ***")
        print("   Gold stash : {}".format(self.inventory["Gold"].balance()))
        if len(self.inventory["Weapons"]) > 0:
            print("   Weapon stash :")
            for w in self.inventory["Weapons"]:
                print("\t\t",w)
        if len(self.inventory["Medicine"]) > 0:
            print("   Medicine stash :")
            for m in self.inventory["Medicine"]:
                print("\t\t",m)
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
        print("\n\t*** You used {} to deal {} damage to the {} ***".format(bestWeapon.name,maxDmg, enemy.name))
        enemy.hp -= maxDmg
        if not enemy.isAlive():
            print("\n\t*** You killed the {} ***".format(enemy.name))
        else:
            print("\n\t*** Remaining HP of the {} is {} ***".format(enemy.name, enemy.hp))
    
    def flee(self, tile):
        #Relocate to random location.
        available_moves = tile.available_moves()
        r = random.randint(0, len(available_moves) - 1)
        deduction = int(0.1 * self.inventory["Gold"].balance())
        print("\n\n\t*** You ran for your life without looking back. You dropped {} coins while fleeing. ***".format(deduction))
        self.inventory["Gold"].removeGold(deduction)
        print("\t*** You have {} gold remaining in your pouch. ***\n\n".format(self.inventory["Gold"].balance()))
        self.do_action(available_moves[r])
    
    def heal(self):
        if len(self.inventory["Medicine"])==0:
            print("\n\t*** You do not have any medicine in your inventory ***\n")
            return
        if self.hp == 100:
            print("\n\t*** You do not need to heal yourself. You have max HP (100). ***\n")
            return
        optimalMedicine = None
        index = 0
        finalResort = None
        finalindex = 0
        minDif = 100
        healingNeeded = 100 - self.hp
        i = 0
        for med in self.inventory["Medicine"]:
            Dif = healingNeeded - med.healing
            if Dif > 0 :
                if minDif > Dif:
                    minDif = Dif
                    optimalMedicine = med
                    index = i
            else:
                finalResort = med
                finalindex = i
            i += 1
        if optimalMedicine == None:
            optimalMedicine = finalResort
            index = finalindex
        self.inventory["Medicine"].pop(index)
        self.hp += optimalMedicine.healing
        if self.hp > 100:
            self.hp = 100
            print("\n\t*** You used Medicine to fully restore your health. ***\n")
        else:
            print("\n\t*** You used Medicine to heal {} HP ***".format(optimalMedicine.healing))
            print("\t*** Your current Health : {} HP ***\n".format(self.hp))

    
    def buy(self, productList):
        while True:
            itemID = input("Enter the item ID you want to buy: ")
            if int(itemID) in productList:
                item = productList[int(itemID)]
                if item.value > self.inventory["Gold"].balance():
                    print("\n\t*** You do not have enough coins to buy {} from the Merchant. Return later with more coins. ***".format(item.name))
                else:
                    self.inventory["Gold"].removeGold(item.value)
                    if isinstance(item, items.Weapon):
                        self.inventory["Weapons"].append(item)
                    elif isinstance(item, items.Medicine):
                        self.inventory["Medicine"].append(item)
                    print("\n\t*** You bought {} for {} gold coins ***".format(item.name, item.value))
            else:
                print("No such item ID exists.")
            keepGoing = input("Want to buy more items (y/n) : ")
            if keepGoing == 'n':
                break
    
    def sell(self, itemID):
        item = self.inventory["Weapons"][itemID-1]
        self.inventory["Gold"].addGold(item.value)
        del self.inventory["Weapons"][itemID-1]
        print("\n\t*** You sold {} to the Merchant and gained {} gold coins ***".format(item.name, item.value))

    def do_action(self, action, **kwargs):
        action_method = getattr(self, action.method.__name__)
        if action_method:
            action_method(**kwargs)

    def __str__(self):
        return "\nI have {} health and {} speed. I am at position ({},{}) and i have the following items in my inventory: {}\n".format(self.hp, self.speed, self.location_x, self.location_y, self.inventorySummary)