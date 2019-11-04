import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    road_eight = room.Room('road_eight', roomPath)
    road_eight.set_description('streach of road', 'This stretch of road continues through the fields, north and south. To the west some hay lies bailed in the fields.')
    road_eight.add_exit('south', 'domains.centrata.firefile_area.fields.road_seven')
    road_eight.add_exit('north', 'domains.centrata.kings_road?domains.centrata.firefile_area.fields.road_eight&domains.centrata.firefile_area.village.south_village&20&0')
    return road_eight
