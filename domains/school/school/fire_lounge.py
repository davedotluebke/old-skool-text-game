import gametools
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    fire_lounge = room.Room('lounge', roomPath, safe=True, indoor=True)
    fire_lounge.set_description('warm lounge', 'You find yourself in a warm room, with red and orange painted stone walls, and pictures of fires and volcanoes. Many confortable chairs are in the room. A grand fireplace stands to the south.')
    fire_lounge.add_adjectives('warm', 'confortable')
    fire_lounge.add_exit('east', 'domains.school.school.fire_kitchen')

    for chairs in range(0, 4):
        c = gametools.clone('domains.school.school.chair')
        c.move_to(fire_lounge)

    fireplace = gametools.clone('domains.school.school.fireplace')
    fireplace.dest = 'domains.school.school.great_hall'
    fireplace.move_to(fire_lounge)
    return fire_lounge
