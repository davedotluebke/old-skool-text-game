import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    street = room.Room('street', roomPath)
    street.set_description('village street', 'You find yourself on a village street. To your west you see a clothiers, and to your east you see a house.')
    street.add_exit('south', 'domains.centrata.village.village_fountain')
    street.add_exit('north', 'domains.centrata.village.north_village')
    street.add_exit('west', 'domains.centrata.village.clothiers')

    clothiers = scenery.Scenery('clothiers', 'clothiers', 'This clothiers sits to the west side of the street.')
    clothiers.add_adjectives('west')
    clothiers.move_to(street, True)

    house = scenery.Scenery('house', 'wooden house', 'This wooden house sits to the east side of the street.')
    house.add_adjectives('wooden', 'east')
    house.add_response(['enter'], 'The door is locked.')
    house.move_to(street, True)
    return street