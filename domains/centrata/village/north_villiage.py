import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    north_village = room.Room('street', roomPath)
    north_village.set_description('village street', 'You find yourself on the north end of the village. There are houses on both sides of the street.')
    north_village.add_exit('south', 'domains.centrata.village.street2')
    north_village.add_exit('north', 'domains.centrata.kings_road?domains.centrata.village.north_village&domains.centrata.village.south_village&20&0')
    north_village.add_exit('east', 'domains.centrata.village.house1')

    house = scenery.Scenery('house', 'wooden house', 'This wooden house sits to the west side of the street.')
    house.add_adjectives('wooden', 'west')
    house.add_response(['enter'], 'The door is locked.')
    house.move_to(north_village, True)
    house_one = scenery.Scenery('house', 'wooden house', 'This wooden house sits to the east side of the street.')
    house_one.add_adjectives('house', 'east')
    house_one.move_to(north_village, True)
    return north_village