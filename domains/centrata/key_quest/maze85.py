import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('passage', roomPath, light=0, indoor=True)
    r.set_description('dark passage','This is a dark passage, a coloumn to the southeast.')
    r.add_exit('southeast', 'domains.centrata.key_quest.maze57')
    r.add_exit('west', 'domains.centrata.key_quest.maze99')
    return r
