import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('passage', roomPath, light=0, indoor=True)
    r.set_description('dark passage','This is a dark passage, with no distinguishing features.')
    r.add_exit('northeast', 'domains.centrata.firefile_area.key_quest.maze47')
    r.add_exit('south', 'domains.centrata.firefile_area.key_quest.maze27')
    return r
