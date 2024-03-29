import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('lawn', roomPath)
    r.set_description('south lawn', 'You stand outside the mansion on the south side. To the west there is a large carriage house.')
    r.add_exit('northwest', 'domains.centrata.mansion.west_lawn')
    r.add_exit('northeast', 'domains.centrata.mansion.east_lawn')

    mansion_scenery_south = scenery.Scenery('mansion', 'sandstone mansion', 'A large wing of the mansion stretches out towards you. Unlike most of the mansion, it is made of wood.', unlisted=True)
    mansion_scenery_south.add_adjectives('sandstone', 'massive')
    r.insert(mansion_scenery_south, True)

    carriage_house_scenery = scenery.Scenery('house', 'carriage house', 'This sandstone carriage house matches the house in material, almost like a minature version. It has a large door for carriages in the front.', unlisted=True)
    carriage_house_scenery.add_adjectives('carriage', 'sandstone')
    r.insert(carriage_house_scenery, True)

    return r
