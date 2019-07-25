import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('passage', roomPath, light=0, indoor=True)
    r.set_description('dark passage','This is a dark and steep passage. Around this time it becomes neccecary to scramble to continue downwards.')
    r.add_exit('northeast', 'domains.centrata.firefile_area.key_quest.maze28')
    r.add_exit('down', 'domains.centrata.firefile_area.key_quest.maze57')
    return r
