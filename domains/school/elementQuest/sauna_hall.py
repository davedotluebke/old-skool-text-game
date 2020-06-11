import room
import gametools
import scenery


def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('hall', roomPath, indoor=True)
    r.set_description( 'hallway', 'You find yourself in a short hallway. At one end there is a glass door, at the obsite end you see a normal wood door.')
    r.add_adjectives('suana', 'short')
    r.add_exit('west', 'domains.school.elementQuest.portrait_gallery')
    r.add_exit('east', 'domians.school.elementQuest.sauna_room')
    
    ice_chest = gametools.clone('domains.school.elementQuest.ice_chest')
    r.insert(ice_chest)
    
    return r
