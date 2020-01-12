import gametools
import room
import scenery
from domains.school.school.hallway import StaffDoorway

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    cliff = room.Room('cliff', pref_id=roomPath)
    cliff.set_description('clifftop', 'You walk out onto a massive clifftop, overlooking an endless evergreen forest carpeted with snow. You see a tiny shack with a pine door.')
    cliff.add_exit('west', 'domains.evergreen.mountaintop.cliff2')

    pine_door = StaffDoorway('door', 'pine door', 'This is a strong pine door.', 'home.scott.house.er31795', allowed_players_list=['scott', 'tate', 'cedric', 'rivques'])
    pine_door.add_adjectives('pine', 'strong')
    pine_door.move_to(cliff, True)
    
    return cliff