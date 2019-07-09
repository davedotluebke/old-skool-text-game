import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('passage', roomPath, light=0)
    r.set_description('dark passage','This is a dark passage. Here the rocks form a ladder that is quite easy to climb.')
    r.add_exit('south', 'domains.centrata.firefile_area.key_quest.maze85')
    r.add_exit('up', 'domains.centrata.firefile_area.key_quest.maze37')
    return r
