import gametools
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    lounge = room.Room('lounge', roomPath, safe=True, indoor=True)
    lounge.set_description('underwater lounge', 'This underwater lounge is surrounded by coral.')
    lounge.add_adjectives('underwater', 'coral', 'water')
    lounge.add_exit('up','domains.school.school.water_kitchen')

    return lounge
