import domains.school.elementQuest.lake_room as lake_room
import room
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    deep_depths = lake_room.LakeRoom_underwater('deep depths', roomPath, 'domains.school.elementQuest.lake_center')
    deep_depths.set_description('deep depths', 'This is the deepest part of the lake. You can barely make out the bottom.')
    deep_depths.add_exit('north', 'domains.school.elementQuest.oysters')
    deep_depths.add_exit('east', 'domains.school.elementQuest.doorway')
    deep_depths.add_exit('south', 'domains.school.elementQuest.rusty_can')
    deep_depths.add_exit('west', 'domains.school.elementQuest.statue')
    
    return deep_depths
