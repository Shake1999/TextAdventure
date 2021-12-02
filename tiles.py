import items, enemies, actions, world
import random

class MapTile:
    """ Abstract Base Class """
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def introduction(self):
        raise NotImplementedError

    def modify_player(self):
        raise NotImplementedError

    def available_moves(self):
        """ Returns all move actions for adjacent tiles """
        moves = []
        if world.tile_exists(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y -1):
            moves.append(actions.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves
    
    def available_actions(self):
        """ Returns all available actions in the current tile """
        options = self.available_moves()
        options.append(actions.ViewInventory())
        options.append(actions.ViewStats())
        options.append(actions.Heal())
        return options

class StartingTile(MapTile):
    def introduction(self):
        return """\n\n\t*** It's your first mission as a Bounty Hunter. 
                Find and kill the Silver Dragon and you will become a famous bounty hunter ***\n"""
    
    def modify_player(self, player):
        pass

class LootTile(MapTile):
    """ Base Loot Tile Class """
    def __init__(self, x, y, item):
        self.item = item
        self.flag = True
        super().__init__(x,y)
    
    def add_loot(self, player):
        raise NotImplementedError
    
    def modify_player(self, player):
        if self.flag:
            self.add_loot(player)
            self.flag = False

class EnemyTile(MapTile):
    """ Base Enemy Tile Class """
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x,y)
    
    def modify_player(self, player):
        if self.enemy.isAlive():
            player.hp -= self.enemy.damage
            print("\t*** {} did {} damage. ***\n".format(self.enemy.name, self.enemy.damage))
            if player.isAlive():
                print("\t*** You have {} HP remaining. ***\n".format(player.hp))
            else:
                print("\t*** You died in the attack. ***\n\t *** THE END ***\n")
    
    def available_actions(self):
        if self.enemy.isAlive():
            return [ actions.Attack(enemy=self.enemy), actions.Flee(tile=self) , actions.Heal()]
        else:
            options = self.available_moves()
            options.append(actions.ViewInventory())
            options.append(actions.ViewStats())
            options.append(actions.Heal())
            return options

class MerchantTile(MapTile):
    """ Base Merchant Tile Class """
    def __init__(self, x, y, productList):
        self.productList = productList
        super().__init__(x,y)
     
    def displayProductList(self):
        raise NotImplementedError
    
    def modify_player(self, player):
        pass

    def available_actions(self):
        options = self.available_moves()
        options.append(actions.ViewInventory())
        options.append(actions.ViewStats())
        options.append(actions.Heal())
        options.append(actions.Buy(productList = self.productList))
        return options

class WepMerchantTile(MerchantTile):
    def __init__(self,x,y):
        w1 = items.Sword(random.randint(50,70), random.randint(170, 190))
        w2 = items.Sword(random.randint(70,90), random.randint(190,220))
        w3 = items.MagicWand(random.randint(60,80), random.randint(200, 250))
        w4 = items.MagicWand(random.randint(80,100), random.randint(250,300))
        w5 = items.Dagger()
        index = 1
        self.productList = {}
        for item in random.sample([w1,w2,w3,w4,w5], 2):
            self.productList[index] = item
            index += 1
        super().__init__(x,y, self.productList)
    
    def displayProductList(self):
        myWindow = "\n\t******* MERCHANT WINDOW *******\n\t*** I am selling the following items ***\n"
        for key in self.productList:
            myWindow += "\t [{}]   {} (Damage : {}) for  {} coins\n".format(key, self.productList[key].name, self.productList[key].damage, self.productList[key].value)
        myWindow += "\n"
        return myWindow
    
    def introduction(self):
        merchantWindow = self.displayProductList()
        intro = "\n\t*** You found a small town. You found lodging for the night and \n\tthe next day you explored the town to discover a Merchant of deadly weapons. ***\n"
        return  intro + merchantWindow

class HerbsMerchantTile(MerchantTile):
    def __init__(self, x, y):
        self.productList = {}
        self.productList[1] = items.Medicine(random.randint(20,30), random.randint(120,130))
        self.productList[2] = items.Medicine(random.randint(50,60), random.randint(150,170))
        super().__init__(x,y, self.productList)
    
    def displayProductList(self):
        myWindow = "\n\t******* MERCHANT WINDOW *******\n\t*** I am selling the following herbs ***\n"
        for key in self.productList:
            myWindow += "\t [{}]   A Herbal Medicine (Healing Amount : {}) for  {} coins\n".format(key, self.productList[key].healing, self.productList[key].value)
        myWindow += "\n"
        return myWindow
    
    def introduction(self):
        merchantWindow = self.displayProductList()
        intro = "\n\t*** You found a small town. You found lodging for the night and \n\tthe next day you explored the town to discover a Merchant of remarkable medicinal herbs. ***\n"
        return  intro + merchantWindow

class RatsTile(EnemyTile):
    def __init__(self, x, y):
        super().__init__(x,y, enemies.HungryRat())

    def introduction(self):
        if self.enemy.isAlive():
            return "\n\t*** A rat surfaces from a cracked wall and charges at you. ***\n"
        else:
            return "\n\t*** There is a dead rotting rat lying in the floor and it smells like death. ***\n"
    
class GargoyleTile(EnemyTile):
    def __init__(self, x, y):
        super().__init__(x,y, enemies.Gargoyle())
    
    def introduction(self):
        if self.enemy.isAlive():
            return """\n\t*** A gigantic and ferocious looking Gargoyle is awaken from his sleep as you ventured closer to it. 
            It is angry and wants to rip you to pieces. ***\n"""
        else:
            return """\n\t*** A still gargoyle lay dead with his eyes wide open ***\n"""

class SilverDragonTile(EnemyTile):
    def __init__(self, x, y):
        super().__init__(x,y, enemies.SilverDragon())

    def introduction(self):
        if self.enemy.isAlive():
            return """\n\t*** You have found the layer of the unforgiving and infamous fire-breathing silver Dragon.
            Defeat the beast in combat to receive the mission bounty or get roasted alive. ***\n"""
        else:
            return """\n\t*** The dead caracass of the giant silver dragon was the beginning of a new journey. ***\n"""
    
    #def modify_player(self, player):
    #    player.victory = True

class DesertedTile(MapTile):
    def introduction(self):
        return "\n\t*** You are venturing through a deserted piece of land. Nothing in sight for miles. ***\n"
    
    def modify_player(self, player):
        pass

class GoldTile(LootTile):
    def __init__(self, x, y):
        self.amount = random.randint(100,150)
        super().__init__(x, y, items.Gold(self.amount))
    
    def introduction(self):
        return "\n\t*** You found {} gold coins hidden behind a rock. No one's looking so you stole it. ***\n".format(self.amount)
    
    def add_loot(self, player):
        player.inventory["Gold"].addGold(self.amount)

class SwordTile(LootTile):
    def __init__(self, x, y):
        dmg = random.randint(30,40)
        val = random.randint(150,160)
        super().__init__(x, y, items.Sword(dmg, val))
    
    def introduction(self):
        return """\n\t*** You found a shiny sword stuck in between rocks. 
        \tYou must be the prophesized one because the sword comes off easily as if it's meant to be. ***\n"""
    
    def add_loot(self, player):
        player.inventory["Weapons"].append(self.item)

class WandTile(LootTile):
    def __init__(self, x, y):
        dmg = random.randint(40,50)
        val = random.randint(150,175)
        super().__init__(x, y, items.MagicWand(dmg, val))
    
    def introduction(self):
        return """\n\t*** You found a wooden shaft which looked weird at first but upon careful examination,
                    you learned that it is a powerful magic wand from centuries ago. ***\n"""
    
    def add_loot(self, player):
        player.inventory["Weapons"].append(self.item)