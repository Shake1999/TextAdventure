from player import Player

class Action():
    def __init__(self, method, name, hotkey, **kwargs):
        self.method = method
        self.hotkey = hotkey
        self.name = name
        self.kwargs = kwargs
    
    def __str__(self):
        return "{}: {}".format(self.hotkey, self.name)

class MoveNorth(Action):
    def __init__(self):
        super().__init__(Player.moveNorth, "Move North", "n")

class MoveSouth(Action):
    def __init__(self):
        super().__init__(Player.moveSouth, "Move South", "s")

class MoveEast(Action):
    def __init__(self):
        super().__init__(Player.moveEast, "Move East", "e")

class MoveWest(Action):
    def __init__(self):
        super().__init__(Player.moveWest, "Move West", "w")

class ViewInventory(Action):
    """ Prints the player's inventory """
    def __init__(self):
        super().__init__(Player.inventorySummary, "View inventory", "i")

class Attack(Action):
    def __init__(self, enemy):
        super().__init__(Player.attack, "Attack", "a", enemy)
