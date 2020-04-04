import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    road_three = room.Room('road_three', roomPath)
    road_three.set_description('streach of road', 'This road makes a sharp turn here. It contiues to the north and the southeast.')
    road_three.add_exit('southeast', 'domains.centrata.fields.road_two')
    road_three.add_exit('north', 'domains.centrata.fields.road_four')
    road_three.add_exit('east', 'domains.centrata.prairie?0&-1')
    return road_three
