import domains.school.elementQuest.lake_room as lake_room
import room
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    oysters_room = lake_room.LakeRoom_underwater('oysters', roomPath, 'domains.school.elementQuest.lake_n')
    oysters_room.set_description('bed of oysters', 'You find yourself by a huge bed of oysters. From a few oysters you can barely make out the shimmer of a pearl.')
    oysters_room.add_exit('west', 'domains.school.elementQuest.seaweed_forest')
    oysters_room.add_exit('east', 'domains.school.elementQuest.course_sand')
    oysters_room.add_exit('south', 'domains.school.elementQuest.deep_depths')

    oyster = gametools.clone('domains.school.elementQuest.oyster')
    oyster.move_to(oysters_room, True)
    
    return oysters_room
