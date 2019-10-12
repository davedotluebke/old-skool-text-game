import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    road_four = room.Room('road_four', roomPath)
    road_four.set_description('streach of road', 'This stretch of road continues through the fields, north and south. To the left of the road a strange staircase descends underground.')
    road_four.add_exit('south', 'domains.centrata.firefile_area.fields.road_three', caution_tape_msg="The road to the south is temporarily closed for repairs. Please take the detour via the carved staircase.")
    road_four.add_exit('north', 'domains.centrata.firefile_area.fields.road_five')
    road_four.add_exit('down', 'domains.centrata.firefile_area.cave.carved_staircase')
    return road_four
