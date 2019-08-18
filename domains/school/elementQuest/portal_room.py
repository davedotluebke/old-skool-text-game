import room
import gametools
import scenery

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('portal room', roomPath, indoor=True)
    r.set_description('dimly lit stone-walled room', 'This room is dimly lit by torches. It has been carved out of the rocks. In the centre there stands a stone portal with a sheet of flame.')
    r.add_names('room')
    r.add_exit('east', 'domains.school.elementQuest.potion_room')
    p = gametools.clone('domains.school.elementQuest.portal')
    p.move_to(r)
    return r
