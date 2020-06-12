import room
import gametools
import thing
import scenery
import doors_and_windows


def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('study', roomPath)
    r.indoor = True
    r.set_description('small study', 'You find yourself in a small study')
    r.add_adjectives('windy')
    r.add_exit('up', 'domains.school.elementQuest.bedroom')
    r.add_exit('west', 'domains.school.elementQuest.living_space')

    desk = gametools.clone('domains.school.elementQuest.desk')
    r.insert(desk)

    chair = gametools.clone('domains.school.elementQuest.chair')
    r.insert(chair)


    return r
