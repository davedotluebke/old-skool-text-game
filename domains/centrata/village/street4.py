import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    street = room.Room('street', roomPath)
    street.set_description('village street', 'You find yourself on a village street. To your north you see an inn, and to your south you see a house.')
    street.add_exit('east', 'domains.centrata.village.village_fountain')
    street.add_exit('west', 'domains.centrata.village.west_village')
    street.add_exit('north', 'domains.centrata.village.inn')

    inn = scenery.Scenery('inn', 'inn', 'This inn stands to the north side of the street.')
    inn.add_adjectives('north')
    inn.move_to(street, True)

    house = scenery.Scenery('house', 'wooden house', 'This wooden house sits to the south side of the street.')
    house.add_adjectives('wooden', 'south')
    house.add_response(['enter'], 'The door is locked.')
    house.move_to(street, True)
    return street