import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    prairie_room = room.Room('woods', roomPath)
    prairie_room.set_description('prairie', 'You find yourself in a tallgrass prairie. You notice a small tree, a group of trees to the south, a group of trees to the north, the back of a building to the west, and a small pond.')
    prairie_room.add_exit('east', 'domains.centrata.prairie?2&6')
    return prairie_room
