import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    south_village = room.Room('street', roomPath)
    south_village.set_description('village street', 
        'You find yourself on the south end of the village. '
        'To your west you see a house, and to your east you see a blacksmith\'s shop.')
    south_village.add_exit('south', 'domains.centrata.firefile_area.fields.road_eight')
    south_village.add_exit('north', 'domains.centrata.firefile_area.village.street1')
    south_village.add_exit('east', 'domains.centrata.firefile_area.village.blacksmith_shop')

    house = scenery.Scenery('house', 'wooden house', 'This wooden house sits to the west side of the street.')
    house.add_adjectives('wooden', 'west')
    house.add_response(['enter'], 'The door is locked.')
    house.move_to(south_village, True)

    blacksmiths_shop = scenery.Scenery('shop', 'blacksmith\'s shop', 'This blacksmith\'s shop stands to the '
        'east side of the street.')
    blacksmiths_shop.add_adjectives('blacksmiths', 'blacksmith\'s', 'east')
    blacksmiths_shop.move_to(south_village, True)
    return south_village