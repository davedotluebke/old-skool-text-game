import gametools
import scenery
import keyed_door
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('gateway', roomPath)
    r.set_description('outside of the gate', 'You stand in front of the gate of the massive standstone mansion to the south. Immaculately trimmed bushes surround the gate to both sides.')
    r.add_exit('north', 'domains.centrata.mansion.approach')

    gate = keyed_door.KeyedDoor('gate', 'iron gate', 'This iron gate looks sturdy. It has spikes on top.', 'domains.centrata.mansion.gate_inside', 'south', 'domains.centrata.mansion.gate_key')
    gate.add_adjectives('iron', 'spiked')
    gate.locked = True
    gate.add_response(['climb'], 'The spikes make it far too difficult.')

    r.insert(gate, True)

    bushes = gametools.clone('domains.centrata.mansion.gate_bushes')
    r.insert(bushes, True)

    # duplicated in gate_inside
    mansion_scenery_north = scenery.Scenery('mansion', 'sandstone mansion', 'With a closer look, this massive sandstone mansion is all the more impressive. ' \
                                      'In the northwest corner there stands a massive turret. A large porch hugs the north side of the house, where a ' \
                                      'wide staircase leads up to a large front door.', unlisted=True)
    mansion_scenery_north.add_adjectives('sandstone', 'massive')
    r.insert(mansion_scenery_north, True)

    turret_scenery = scenery.Scenery('turret', 'massive turret', 'This massive turret stretches up from the ground to the third storey of the mansion. ', unlisted=True)
    turret_scenery.add_adjectives('massive')
    r.insert(turret_scenery, True)

    porch_scenery = scenery.Scenery('porch', 'large porch', 'This large porch extends from the front of the mansion.', unlisted=True)
    porch_scenery.add_adjectives('large', 'front')
    r.insert(porch_scenery, True)

    return r
