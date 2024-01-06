import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('driveway', roomPath)
    r.set_description('driveway', 'You find yourself on a driveway through the forest, leading south up a hill towards a grandiose sandstone mansion.')
    r.add_exit('north', 'domains.school.forest.waterfall')
    r.add_exit('south', 'domains.centrata.mansion.gate_outside')
    return r
