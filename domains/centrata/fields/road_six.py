import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    road_six = room.Room('road_six', roomPath)
    road_six.set_description('streach of road', 'This stretch of road continues through the fields, north and south. You notice a large sign to the side of the road.')
    road_six.add_exit('south', 'domains.centrata.fields.road_five')
    road_six.add_exit('north', 'domains.centrata.fields.road_seven')
    road_six.add_exit('east', 'domains.centrata.fields.questentry')

    sign = scenery.Scenery('sign', 'large wooden sign', 'This sign is made of solid wood and painted on with golden paint. It appears to say something on it.')
    sign.add_response(['read'], "The sign reads:\n**Wanted:** Skilled swordusers to help defeat serpents. Inquire to the east. Rewarded handsomely.")
    sign.add_adjectives('wooden')
    sign.move_to(road_six, force_move=True)
    return road_six
