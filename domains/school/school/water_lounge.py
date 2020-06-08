import gametools
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    lounge = room.Room('lounge', roomPath, safe=True, indoor=True)
    lounge.set_description('underwater lounge', 'This underwater lounge is surrounded by coral. To the south there lies the backside of a gushing waterfall.')
    lounge.add_adjectives('underwater', 'coral', 'water')
    lounge.add_exit('up','domains.school.school.water_kitchen')
    lounge.add_exit('south', 'domains.school.forest.waterfall')

    return lounge
