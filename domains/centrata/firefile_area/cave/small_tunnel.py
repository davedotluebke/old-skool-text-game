import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('tunnel', roomPath, light=0, indoor=True)
    r.set_description('small tunnel', 'This small tunnel looks as if it was carved carefully from the rock. You hear the sound of rushing water to the south.')
    r.add_exit('south', 'domains.school.forest.underground_waterfall')
    r.add_exit('north', 'domains.centrata.firefile_area.cave.carved_staircase')

    return r
