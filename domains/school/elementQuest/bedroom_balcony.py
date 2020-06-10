import room
import gametools
import scenery
import doors_and_windows

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = room.Room('balcony', roomPath)
    r.set_description('balcony', 'This is a large balcony overlooking some tall, steep mountains. You notice a large number of birdfeeders here.')
    r.add_adjectives('bedroom', 'birdfeeder', 'mountain', 'tower')
    
    east_door = doors_and_windows.Door('door', 'glass door', 'This tinted glass door leads back into the tower.', 'domains.school.elementQuest.bedroom', 'east')
    east_door.add_adjectives('glass', 'bedroom')
    r.insert(east_door)

    # TODO: add birdfeeders here
    
    return r