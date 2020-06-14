import gametools
import room
import doors_and_windows

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    entryway = room.Room('hallway', pref_id=roomPath, indoor=True, safe=True)
    entryway.set_description('long hallway','You find yourself in a hallway with four doors off of it. To the south you see a larger room.')
    entryway.add_exit('south', 'home.scott.house.lr31795')

    pine_door = doors_and_windows.Door('door', 'strong pine door', 'This is a strong pine door on the northwest side of the hallway.', 'domains.evergreen.mountaintop.cliff', 'northwest', ['scott'])
    pine_door.add_adjectives('pine')
    pine_door.move_to(entryway, True)

    stone_door = doors_and_windows.Door('door', 'stone door', 'This is a sturdy stone door on the southeast side of the hallway.', 'home.scott.house.descents', 'southeast', ['scott'])
    stone_door.add_adjectives('stone')
    stone_door.move_to(entryway, True)

    return entryway
