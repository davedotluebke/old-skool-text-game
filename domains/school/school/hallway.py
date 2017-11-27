import gametools
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    hallway = room.Room('hallway', roomPath, safe=True)
    hallway.indoor = True
    hallway.set_description('staff office hallway', 'This hallway leads to all of the staff offices. It is very blank on the walls, however the walls themselves are intricate and have little carved patterns in them.')
    hallway.add_adjectives('staff', 'office')
    hallway.add_exit('south', 'domains.school.school.gallery')
    return hallway
