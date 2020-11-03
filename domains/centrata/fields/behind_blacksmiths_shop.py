import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    prairie_room = room.Room('woods', roomPath)
    prairie_room.set_description('prairie', 'You find yourself in a tallgrass prairie. You notice a small pond, a group of trees to the west, a big herd of bison to the north, and the back of a building to the west.')
    prairie_room.add_exit('east', 'domains.centrata.orc_quest.prairie?2&5')
    prairie_room.add_exit('south', 'domains.centrata.orc_quest.prairie?1&4')
    return prairie_room
