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
    cliff.add_exit('east', 'domains.evergreen.mountaintop.cliff')
    
    cottage = scenery.Scenery('cottage', 'small wood cottage', 'You see a small wood cottage, with a pine wood door.')
    cottage.move_to(cliff, True)

    spruce_door = StaffDoorway('door','spruce door','you see a small, strong, spruce door,with a golden key hole.', 'home.tate.cottage', allowed_players_list=['tate'])
    spruce_door.add_adjectives('spruce','strong','small')
    spruce_door.move_to(cliff,True)

    return cliff