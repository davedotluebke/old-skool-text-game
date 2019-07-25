import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    road_seven = room.Room('road_seven', roomPath)
    road_seven.set_description('streach of road', 'This stretch of road continues through the fields, north and south. You see a small hill to your west.')
    road_seven.add_exit('south', 'domains.centrata.firefile_area.fields.road_six')
    road_seven.add_exit('north', 'domains.centrata.firefile_area.fields.road_eight')
    return road_seven
