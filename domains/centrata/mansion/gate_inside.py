import gametools
import scenery
import keyed_door
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('gateway', roomPath)
    r.set_description('inside of the gate', 'You stand inside the gate of the massive standstone mansion to the south.')

    gate = keyed_door.KeyedDoor('gate', 'iron gate', 'This iron gate looks sturdy. It has spikes on top.', 'domains.centrata.mansion.gate_outside', 'north', 'domains.centrata.mansion.gate_key')
    gate.add_adjectives('iron', 'spiked')
    gate.locked = True
    gate.add_response(['climb'], 'The spikes make it far too difficult.')

    r.insert(gate, True)

    return r
