import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('cavern', roomPath, light=0, indoor=True)
    r.set_description('deep cavern','This is a large, deep cavern. You can see a small pool of water at the bottom.')
    r.add_exit('east', 'domains.centrata.firefile_area.key_quest.maze16')
    r.add_exit('west', 'domains.centrata.firefile_area.key_quest.maze58')
    r.add_exit('north', 'domains.centrata.firefile_area.key_quest.maze75')
    r.add_exit('down', 'domains.centrata.firefile_area.key_quest.maze82')
    return r
