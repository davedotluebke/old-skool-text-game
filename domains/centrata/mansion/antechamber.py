import gametools
import scenery
import room
import keyed_door

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('antechamber', roomPath, indoor=True)
    r.set_description('spacious antechamber', 'You stand inside a spacious antechamber. The walls are panelled with mahogany. There are doors to the north and the south.')
    
    antechamber_door = keyed_door.KeyedDoor('door', 'mahogany door', 'This mahogany door has bevelled edges around two indented panels.', 'domains.centrata.mansion.parlour', 'south', 'domains.centrata.mansion.interior_door_key')
    antechamber_door.add_adjectives('mahogany', 'wooden', 'bevelled')
    antechamber_door.unlocked = True
    r.insert(antechamber_door, True)
    
    front_door = keyed_door.KeyedDoor('door', 'front door', 'This grandiose front door is made of mahogany. It has elaborate carvings of dragons on it.', 'domains.centrata.mansion.porch', 'north', 'domains.centrata.mansion.house_key')
    front_door.add_adjectives('large', 'grandiose', 'front')
    front_door.locked = True
    r.insert(front_door, True)
    
    chandelier = gametools.clone('domains.centrata.mansion.chandelier2')
    r.insert(chandelier, True)

    return r
