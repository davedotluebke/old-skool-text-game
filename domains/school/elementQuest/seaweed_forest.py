import domains.school.elementQuest.lake_room as lake_room
import room
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    seaweed_forest = lake_room.LakeRoom_underwater('seaweed forest', roomPath, 'domains.school.elementQuest.lake_nw')
    seaweed_forest.set_description('seaweed forest', 'You find yourself in a dense forest of seaweed. It so thick you have trouble looking around it.')
    seaweed_forest.add_exit('south', 'domains.school.elementQuest.statue')
    seaweed_forest.add_exit('east', 'domains.school.elementQuest.oysters')
    
    return seaweed_forest
