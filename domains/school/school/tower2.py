import room
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    towerstairs = room.Room('towerstairs', roomPath, safe=True, indoor=True)
    towerstairs.set_description('spiral staircase leading up the tower', 
    'You find yourself in an enormous tower with winding stairs leading up it. There is a small door to the west.')
    towerstairs.add_names('stairs')
    towerstairs.add_adjectives('tower', 'spiral')
    towerstairs.add_exit('down', 'domains.school.school.back_entrance', caution_tape_msg='The stairway down is blocked with lots of wood. It is clearly being renovated.')
    towerstairs.add_exit('up', 'domains.school.school.air_bridge')
    towerstairs.add_exit('west', 'domains.school.school.classroom_hallway')
    return towerstairs
