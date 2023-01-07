import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    cavern = room.Room('cavern', roomPath)
    cavern.set_description('rough-walled cavern', 'This cavern has rough walls. You also notice a ladder carved into the walls.')
    cavern.add_exit('east', 'domains.endless_terrain.endless_caverns?1&10000&0')
    cavern.add_exit('west', 'domains.endless_terrain.endless_caverns?-1&10000&0')
    cavern.add_exit('up', 'home.johanna.house.descents')
    return cavern