import room
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    classroom = room.Room('classroom', roomPath, indoor=True)
    classroom.set_description('medium-sized classroom', 'This is a medium-sized classroom. A large door stands to the north. To the south there stands a large desk, with a small door behind it.')
    classroom.add_exit('north', 'domains.school.school.classroom_hallway')
    
    profsun = gametools.clone('domains.school.school.profsun')
    classroom.insert(profsun)
    
    return classroom