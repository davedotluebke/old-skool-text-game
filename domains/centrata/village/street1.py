import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    street = room.Room('street', roomPath)
    street.set_description('village street', 'You find yourself on a village street. To your west you see a general store, and to your east you see a tailor\'s.')
    street.add_exit('south', 'domains.centrata.village.south_village')
    street.add_exit('north', 'domains.centrata.village.village_fountain')
    street.add_exit('west', 'domains.centrata.village.general_store')
    street.add_exit('east', 'domains.centrata.village.tailors')

    general_store = scenery.Scenery('store', 'general store', 'This general store sits to the west side of the street.')
    general_store.add_adjectives('general', 'west')
    general_store.move_to(street, True)

    tailors = scenery.Scenery('tailors', 'tailor\'s shop', 'This tailor\'s shop stands to the east side of the street.')
    tailors.add_adjectives('tailor\'s', 'tailors')
    tailors.add_names('shop', 'tailor\'s')
    tailors.move_to(street, True)
    return street