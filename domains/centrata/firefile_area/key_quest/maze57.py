import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('passage', roomPath, light=0, indoor=True)
    r.set_description('dark passage','This is a dark passage. It is very rocky and steep')
    r.add_exit('east', 'domains.centrata.firefile_area.key_quest.maze82')
    r.add_exit('up', 'domains.centrata.firefile_area.key_quest.maze49')
    r.add_exit('west', 'domains.centrata.firefile_area.key_quest.maze85')
    return r
