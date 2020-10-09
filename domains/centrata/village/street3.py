import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    street = room.Room('street', roomPath)
    street.set_description('village street', 'You find yourself on a village street. To your north you see an armourer, and to your south you see a fletcher.')
    street.add_exit('west', 'domains.centrata.village.village_fountain')
    street.add_exit('east', 'domains.centrata.village.east_village')
    street.add_exit('north', 'domains.centrata.village.armourer')
    street.add_exit('south', 'domains.centrata.village.fletchers_shop')

    armourer = scenery.Scenery('armourer', 'armourer\'s shop', 'This armourer stands to the north side of the street.')
    armourer.add_adjectives('north')
    armourer.move_to(street, True)

    fletchers = scenery.Scenery('fletcher\'s', 'fletcher\'s shop', 'This fletcher\'s shop stands to the north side of the street.')
    fletchers.add_adjectives('south')
    fletchers.move_to(street, True)
    return street