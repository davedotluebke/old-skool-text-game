import gametools
import scenery
import keyed_door
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('porch', roomPath)
    r.set_description('large porch', 'You stand on a large porch, overlooking the forest to the north. A staircase to the north leads down into a small yard. To the south, a large front door leads into the mansion.')
    r.add_exit('north', 'domains.centrata.mansion.gate_inside')

    front_door = keyed_door.KeyedDoor('door', 'front door', 'This grandiose front door is made of mahogany. It has elaborate carvings of dragons on it.', 'domains.centrata.mansion.antechamber', 'south', 'domains.centrata.mansion.house_key')
    front_door.add_adjectives('large', 'grandiose', 'front')
    front_door.locked = True

    r.insert(front_door, True)

    dragon_carvings = scenery.Scenery('carvings', 'dragon carvings', 'These carvings of dragons look quite detailed, almost as if they were based on specific creatures.', unlisted=True)
    dragon_carvings.add_adjectives('dragon', 'detailed')
    r.insert(dragon_carvings, True)

    return r
