import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    road_seven = room.Room('road_seven', roomPath)
    road_seven.set_description('streach of road', 'This stretch of road continues through the fields, north and south. You see a small hill to your west.')
    road_seven.add_exit('south', 'domains.centrata.fields.road_six')
    road_seven.add_exit('north', 'domains.centrata.fields.road_eight')
    road_seven.add_exit('east', 'domains.centrata.orc_quest.prairie?0&3')
    return road_seven
