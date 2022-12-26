import room
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    hallway = room.Room('hallway', roomPath, safe=True, indoor=True)
    hallway.set_description('long hallway', 'This is a long hallway with many doors off of it. The one to the south catches your eye.')
    hallway.add_exit('west', 'domains.school.school.towerstairs')
    hallway.add_exit('south', 'domains.school.school.classroom1', caution_tape_msg='This doorway is locked. A note on it reads: I am currently out.')
    hallway.add_exit('east', 'domains.school.school.tower2')
    return hallway
