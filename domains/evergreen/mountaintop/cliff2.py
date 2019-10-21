import gametools
import room
import scenery
from domains.school.school.hallway import StaffDoorway

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    cliff = room.Room('cliff', pref_id=roomPath)
    cliff.set_description('clifftop', 'You walk out onto a massive clifftop, overlooking an endless evergreen forest carpeted with snow. You see a small wood cottage with a small pine door.')
    cottage = scenery.Scenery('cottage', 'small wood cottage', 'You see a small wood cottage, with a pine wood door.')
    cottage.move_to(cliff, True)
    pine_door = StaffDoorway('door')
    cliff.add_exit('east', 'domains.evergreen.mountaintop.cliff')

    return cliff