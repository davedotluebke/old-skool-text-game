import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('passage', roomPath, light=0, indoor=True)
    r.set_description('dark passage','This is a dark passage, with a column to the nourthwest')
    r.add_exit('east', 'domains.centrata.key_quest.maze47')
    r.add_exit('west', 'domains.centrata.key_quest.maze81')
    return r
