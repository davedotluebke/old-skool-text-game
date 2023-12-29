import gametools
import scenery
import keyed_door
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('gateway', roomPath)
    r.set_description('outside of the gate', 'You stand in front of the gate of the massive standstone mansion to the south.')
    r.add_exit('north', 'domains.centrata.mansion.approach')

    gate = keyed_door.KeyedDoor('gate', 'iron gate', 'This iron gate looks sturdy. It has spikes on top.', 'domains.centrata.mansion.gate_inside', 'south', 'domains.centrata.mansion.gate_key')
    gate.add_adjectives('iron', 'spiked')
    gate.locked = True
    gate.add_response(['climb'], 'The spikes make it far too difficult.')

    r.insert(gate, True)

    key = gametools.clone('domains.centrata.mansion.gate_key')
    r.insert(key, True)

    return r
