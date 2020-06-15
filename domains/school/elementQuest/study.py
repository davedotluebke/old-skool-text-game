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
    r.set_description('small study', 'You find yourself in a small study with a dark wood desk with a old wooden chair behind it. It looks like it has not been used in years.')
    r.add_adjectives('small')
    r.add_exit('down', 'domains.school.elementQuest.bedroom')
    r.add_exit('east', 'domains.school.elementQuest.living_space')

    desk = gametools.clone('domains.school.elementQuest.desk')
    r.insert(desk)

    chair = gametools.clone('domains.school.elementQuest.chair')
    r.insert(chair)


    return r
