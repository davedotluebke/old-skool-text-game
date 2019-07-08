import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    road_five = room.Room('road_five', roomPath)
    road_five.set_description('streach of road', 'This stretch of road continues through the fields, north and south. To the far west you catch a glimpse of a far-off mountain range.')
    road_five.add_exit('south', 'domains.centrata.firefile_area.fields.road_four')
    road_five.add_exit('north', 'domains.centrata.firefile_area.fields.road_six')
    return road_five
