import gametools
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = room.Room("office", roomPath, safe=True, indoor=True)
    r.set_description("empty office", "This is the most boring office you have ever seen.")
    r.add_adjectives("boring")
    r.add_exit("northeast", "domains.school.school.hallway")
    return r
