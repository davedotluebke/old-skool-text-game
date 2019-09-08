import gametools
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    landing = room.Room('landing', safe=True, pref_id=roomPath)
    landing.indoor = True
    landing.set_description('elevated landing overlooking the Great Hall', 'You stand on the landing of a grand staircase, overlooking the cavernous Great Hall. From here the staircase splits into two smaller staircases,--to the northeast and southeast--which lead to the next level.')
    landing.add_exit('northeast', 'domains.school.school.gallery')
    landing.add_exit('southeast', 'domains.school.school.library')
    landing.add_exit('west', 'domains.school.school.great_hall')
    return landing
