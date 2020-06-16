import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    sea_otter_hall = room.Room('sea_otter_hall', roomPath, safe=True, indoor=True)
    sea_otter_hall.set_description('blue painted room', 'This room is painted blue from floor to ceiling. On the walls you notice a few carvings of sea otters.')
    sea_otter_hall.add_adjectives('blue', 'painted', 'otter')
    sea_otter_hall.add_exit('south', 'domains.school.school.hallway')
    sea_otter_hall.add_exit('north', 'home.tate.tatelivingspace')
    return sea_otter_hall