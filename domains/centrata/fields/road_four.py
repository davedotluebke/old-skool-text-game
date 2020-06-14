import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    road_four = room.Room('road_four', roomPath)
    road_four.set_description('streach of road', 'This stretch of road continues through the fields, north and south. To the left of the road a strange staircase descends underground.')
    road_four.add_exit('south', 'domains.centrata.fields.road_three')
    road_four.add_exit('north', 'domains.centrata.fields.road_five')
    road_four.add_exit('down', 'domains.centrata.cave.carved_staircase')
    road_four.add_exit('east', 'domains.centrata.prairie?0&0')
    return road_four
