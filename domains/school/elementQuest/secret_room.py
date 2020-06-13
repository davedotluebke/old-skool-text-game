import room
import gametools
import scenery
import doors_and_windows

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = room.Room('balcony', roomPath)
    r.set_description('balcony', 'This is a crumbling balcony halfway up the tower. In front of you there is a giant drop down from the tower. '
    'A large pedistal stands in the centre of the balcony, with a peculiarly-shaped space on it.')
    r.add_adjectives('crumbling')

    east_door = doors_and_windows.Door('door', 'stone door', 'This is a stone door carved into the wall.', 'domains.school.elementQuest.portrait_gallery', 'east', [])
    east_door.add_adjectives('stone','carved')
    r.insert(east_door)

    pedistal = gametools.clone('domains.school.elementQuest.pedistal')
    r.insert(pedistal)

    return r
