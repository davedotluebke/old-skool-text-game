import room
import scenery
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    entryway = room.Room('entryway', roomPath)
    entryway.indoor = True
    entryway.set_description('barren entryway', 'The dusty entryway has one chandelier hanging from the ceiling.')
    entryway.add_exit('east', 'domains.school.forest.woods')
    entryway.add_exit('southwest', 'domains.school.forest.kitchen')
    entryway.add_exit('south', 'domains.school.forest.hallway')

    chandelier = scenery.Scenery('chandelier', 'chandalier', 'This chandalier hangs very high from the ceiling.', unlisted=True)
    chandelier.move_to(entryway, True)

    return entryway