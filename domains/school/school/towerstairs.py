import room
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    towerstairs = room.Room('towerstairs', roomPath, safe=True)
    towerstairs.indoor = True
    towerstairs.set_description('spiral staircase leading up the tower', 'You find yourself in an enormous tower with winding stairs leading up it. There is a small door to the east.')
    towerstairs.add_names('stairs')
    towerstairs.add_adjectives('tower', 'spiral')
    towerstairs.add_exit('down', 'domains.school.school.library')
    towerstairs.add_exit('up', 'domains.school.school.lookout')
    return towerstairs
