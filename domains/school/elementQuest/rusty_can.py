import domains.school.elementQuest.lake_room as lake_room
import room
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    smooth_sand = lake_room.LakeRoom_underwater('smooth sand', roomPath, 'domains.school.elementQuest.lake_s')
    smooth_sand.set_description('smooth sand', 'You find yourself surrounded by a coating of smooth sand. A rusty canister sits to one side.')
    smooth_sand.add_exit('west', 'domains.school.elementQuest.shallow_shore')
    smooth_sand.add_exit('north', 'domains.school.elementQuest.deep_depths')
    smooth_sand.add_exit('east', 'domains.school.elementQuest.inflow')

    rusty_can = gametools.clone('domains.school.elementQuest.rusty_can_obj')
    smooth_sand.insert(rusty_can, True)
    
    return smooth_sand
