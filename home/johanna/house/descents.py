import gametools
import scenery
import room
import doors_and_windows

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('tunnel', roomPath)
    r.set_description('tunnel', 'This tunnel turns downwards here, descending into a cavern below. There is a door to the west.')
    r.add_exit('down', 'domains.endless_terrain.endless_caverns?0&10000&0')
    
    door = doors_and_windows.Door('door', 'stone door', 'This is a sturdy stone door.', 'home.johanna.house.er31795', 'west', ['johanna'])
    door.add_adjectives('stone', 'sturdy')
    door.move_to(r, True)
    return r