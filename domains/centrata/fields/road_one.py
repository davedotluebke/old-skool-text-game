import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    road_one = room.Room('road_one', roomPath)
    road_one.set_description('streach of road', 'This road continues through the prairie, northwest and the southeast.')
    road_one.add_exit('northwest', 'domains.centrata.fields.road_two')
    road_one.add_exit('southeast', 'domains.centrata.fields.school_gates')
    road_one.add_exit('north', 'domains.centrata.prairie?1&-2')
    road_one.add_exit('east', 'domains.centrata.prairie?2&-3')
    return road_one
