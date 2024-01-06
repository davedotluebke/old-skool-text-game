import gametools
import scenery
import keyed_door
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('lawn', roomPath)
    r.set_description('west lawn', 'You stand outside the mansion on the west side. To the south there is a large carriage house.')
    r.add_exit('northeast', 'domains.centrata.mansion.gate_inside')
    r.add_exit('southeast', 'domains.centrata.mansion.south_lawn')

    mansion_scenery_west = scenery.Scenery('mansion', 'sandstone mansion', 'In the northwest corner of the mansion there stands a massive turret. ' \
                                      'A wing stretches out to the south.', unlisted=True)
    mansion_scenery_west.add_adjectives('sandstone', 'massive')
    r.insert(mansion_scenery_west, True)

    # duplicated in gate_inside
    turret_scenery = scenery.Scenery('turret', 'massive turret', 'This massive turret stretches up from the ground to the third storey of the mansion.', unlisted=True)
    turret_scenery.add_adjectives('massive')
    r.insert(turret_scenery, True)

    carriage_house_scenery = scenery.Scenery('house', 'carriage house', 'This sandstone carriage house matches the house in material, almost like a minature version. It has a large door for carriages in the front.', unlisted=True)
    carriage_house_scenery.add_adjectives('carriage', 'sandstone')
    r.insert(carriage_house_scenery, True)

    carriage_door = keyed_door.KeyedDoor('door', 'carriage door', 'This carriage door leads from the west lawn into the carriage house.', 'domains.centrata.mansion.carriage_house', 'south', 'domains.centrata.mansion.gate_key')
    carriage_door.add_adjectives('carriage')

    r.insert(carriage_door, True)

    return r
