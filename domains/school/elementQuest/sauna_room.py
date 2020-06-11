import room
import gametools
import scenery


def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('sauna', roomPath, indoor=True)
    r.set_description( 'sauna', 'You go through a glass door and enter a suana.')
    r.add_adjectives('suana', 'short')
    r.add_exit('west', 'domains.school.elementQuest.sauna_hall')
    r.add_exit('east', 'domians.school.elementQuest.sauna_balcony')
    
    ice_melter = gametools.clone('domains.school.elementQuest.ice_melter')
    r.insert(ice_melter)
     
    return r
