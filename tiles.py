import items, enemies, actions, world

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
        return options

class StartingTile(MapTile):
    def introduction(self):
        return """It's your first mission as a Bounty Hunter. 
                Find and kill the Silver Dragon and you will become a famous bounty hunter"""
    
    def modify_player(self, player):
        pass

class LootTile(MapTile):
    """ Base Loot Tile Class """
    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x,y)
    
    def add_loot(self, player):
        player.inventory.append(self.item)
    
    def modify_player(self, player):
        self.add_loot(player)

class EnemyTile(MapTile):
    """ Base Enemy Tile Class """
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x,y)
    
    def modify_player(self, player):
        if self.enemy.isAlive():
            totEnemyDamage = self.enemy.damage * self.enemy.speed
            totPlayerDamage = player.weapon.damage * player.speed
            pass
    
    def available_actions(self):
        if self.enemy.isAlive():
            return actions.Attack(enemy=self.enemy)
        else:
            return self.available_moves()

class MerchantTile(MapTile):
    """ Base Merchant Tile Class """
    def __init__(self, x, y, productList):
        self.productList = productList
        self.displayProductList()
        super().__init__(x,y)
    
    def displayProductList(self):
        print(" I am selling the following items ")
        for item in self.productList:
            print(item.name + "\t" + item.value)
    
    def processTransaction(self, itemID, player):
        itemBought = self.productList.pop(itemID)
        player.inventory.gold -= itemBought.value
        player.inventory += itemBought
    
    def modify_player(self, player):
        self.processTransaction(_, player)

class RatsTile(EnemyTile):
    def __init__(self, x, y):
        super().__init__(x,y, enemies.HungryRat())

    def introduction(self):
        if self.enemy.isAlive():
            return " A rat surfaces from a cracked wall and chares at you. "
        else:
            return " There is a dead rotting rat lying in the floor and it smells like death. "
    
class GargoyleTile(EnemyTile):
    def __init__(self, x, y):
        super().__init__(x,y, enemies.Gargoyle())
    
    def introduction(self):
        if self.enemy.isAlive():
            return """ A gigantic and ferocious looking Gargoyle is awaken from his sleep as you ventured closer to it. 
            It is angry and wants to rip you to pieces"""
        else:
            return """ A still gargoyle lay dead with his eyes wide open """

class GoldTile(LootTile):
    def __init__(self, x, y):
        super().__init__(x, y, items.Gold(100))
    
    def introduction(self):
        return " You found gold in the room. No one's looking so you stole it."

class DesertedTile(MapTile):
    def introduction(self):
        return " You are venturing through a deserted piece of land. Nothing in sight for miles. "
    
    def modify_player(self, player):
        pass

class SilverDragonTile(EnemyTile):
    def __init__(self, x, y):
        super().__init__(x,y, enemies.SilverDragon())

    def introduction(self):
        if self.enemy.isAlive():
            return """ You have found the layer of the unforgiving and infamous fire-breathing silver Dragon.
            Defeat the beast in combat to receive the mission bounty or get roasted alive. """
        else:
            return """ The dead caracass of the giant silver dragon was the beginning of a new journey."""
    
    def modify_player(self, player):
        player.victory = True