import gametools
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    entrance = room.Room('entrance', roomPath)
    entrance.indoor = True
    entrance.set_description('entrance', 'This room has a ladder in the center going up. You can see light from above you. To the north there is a crawlway.')
    entrance.add_exit('up', 'domains.school.elementQuest.path_choice')
    entrance.add_exit('north', 'domains.school.dungeon.small_tunnel')
    return entrance