import room
import gametools
import scenery

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = room.Room('bridge', roomPath)
    r.set_description('bridge', 'This is a large stone bridge over a large chasam. '
    'A rainbow is being projected onto it from a prism to the east. To the west the '
    'bridge ends at a plaform beside a mountain.')
    r.add_adjectives('rainbow')
    r.add_exit('east', 'domains.school.elementQuest.secret_room')
    r.add_exit('west', 'domains.school.elementQuest.air_portal')
    return r
