import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = room.Room('carved_staircase', roomPath, indoor=True)
    r.set_description('carved staircase', 'You find yourself on a narrow, spiraling staircase carved carefully from the rock.')
    r.add_exit('south', 'domains.centrata.firefile_area.cave.small_tunnel')
    r.add_exit('up', 'domains.centrata.firefile_area.fields.road_four')
    return r