import room
import scenery
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    hallway = room.Room('hallway')
    hallway.set_description('dusty hallway', 'This hallway has dusty walls made of wood. It is dim.')
    hallway.add_exit('north', 'domains.school.forest.entryway')
    hallway.add_exit('northwest', 'domains.school.forest.kitchen')
    hallway.add_exit('southeast', 'domains.school.forest.bedroom')
    return hallway
