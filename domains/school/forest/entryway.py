import room
import scenery
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    entryway = room.Room('entryway')
    entryway.set_description('barren entryway', 'The dusty entryway has one chandelier hanging from the celing.')
    entryway.add_exit('east', 'domains.school.forest.woods')
    entryway.add_exit('southwest', 'domains.school.forest.kitchen')
    entryway.add_exit('south', 'domains.school.forest.hallway')

    return entryway