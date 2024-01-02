import gametools
import scenery
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('office', roomPath, indoor=True)
    r.set_description('mahogany-panelled office', 'You stand in a mahogany-panelled office with books surrounding you on every side. A large oak desk fills the centre of the room. To the east, a large bay window looks out over the lawn.')
    r.add_exit('west', 'domains.centrata.mansion.safe')

    office_bookcase = gametools.clone('domains.centrata.mansion.office_bookshelf')
    r.insert(office_bookcase, True)

    return r
