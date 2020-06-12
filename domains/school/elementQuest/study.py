import room
import gametools
import thing
import scenery
import doors_and_windows


def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('nursury', roomPath)
    r.indoor = True
    r.set_description('multi-porpuse nursery', 'You enter a small carpeted room. On the north side you see a changing table with a painting hanging over it and, a cradle and a some cabinits. On the south side of the room you see five flower pots')
    r.add_adjectives('windy')
    r.add_exit('up', 'domains.school.elementQuest.armor_museum')
    r.add_exit('down', 'domains.school.elementQuest.statue_room')

    prism = gametools.clone('domains.school.elementQuest.prism')

    return r
