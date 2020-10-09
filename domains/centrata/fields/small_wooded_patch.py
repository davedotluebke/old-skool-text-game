import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    wooded_patch = room.Room('woods', roomPath)
    wooded_patch.set_description('small wooded patch', 'This small wooded patch is relativly open. You see the wooded wall of a building to the north.')
    wooded_patch.add_exit('east', 'domains.centrata.prairie?1&4')
    wooded_patch.add_exit('west', 'domains.centrata.fields.road_eight')
    wooded_patch.add_exit('south', 'domains.centrata.prairie?0&3')
    return wooded_patch
