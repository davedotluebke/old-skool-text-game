import gametools
import scenery
import room
from domains.centrata.mansion.safe_door import SafeDoorInside

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('safe', roomPath, indoor=True)
    r.set_description('inside of a safe', 'You stand inside a walk-in safe. The walls are a plain white, discoloured a bit by the damp air. There are several shelves built into the walls.')
    
    safe_door = SafeDoorInside()
    r.insert(safe_door)

    safe_shelves = gametools.clone('domains.centrata.mansion.safe_shelves')
    r.insert(safe_shelves, True)

    return r
