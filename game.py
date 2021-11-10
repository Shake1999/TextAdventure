import world
from player import Player

def play():
    world.load_tiles()
    player = Player()
    print(player)
    room = world.tile_exists(player.location_x, player.location_y)
    print(room.introduction())
    while player.isAlive() and not player.victory:
        # Game Loop starting
        room = world.tile_exists(player.location_x, player.location_y)
        room.modify_player(player)
        if player.isAlive() and not player.victory:
            print("Choose an action:\n")
            availableActions = room.available_actions()
            for action in availableActions:
                print(action)
            action_input = input("Action:")
            for action in availableActions:
                if action_input == action.hotkey:
                    player.do_action(action, **action.kwargs)
                    break

if __name__ == "__main__":
    play()