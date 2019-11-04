import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    intersection = room.Room('intersection', roomPath)
    intersection.set_description('intersection', 'You make your way into an intersection in the centre of the village. A small fountain stands in the middle of it.')
    intersection.add_exit('south', 'domains.centrata.firefile_area.village.street1')
    intersection.add_exit('north', 'domains.centrata.firefile_area.village.street2')
    intersection.add_exit('west', 'domains.centrata.firefile_area.village.street4')
    intersection.add_exit('east', 'domains.centrata.firefile_area.village.street3')

    fountain = scenery.Scenery('fountain', 'iron fountain', 'This fountain stands in the middle of the street. It has water flowing through it.')
    fountain.add_adjectives('iron', 'central')
    fountain.add_response(['drink'], 'You take a drink from the fountain.')
    fountain.move_to(intersection, True)
    return intersection