import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    road_two = room.Room('road_two', roomPath)
    road_two.set_description('streach of road', 'This road continues through the prairie, northwest and the southeast. You notice a big clump of trees to the south.')
    road_two.add_exit('northwest', 'domains.centrata.fields.road_three')
    road_two.add_exit('southeast', 'domains.centrata.fields.road_one')
    road_two.add_exit('north', 'domains.centrata.orc_quest.prairie?0&-1')
    road_two.add_exit('east', 'domains.centrata.orc_quest.prairie?1&-2')
    return road_two
