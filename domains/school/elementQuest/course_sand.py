import domains.school.elementQuest.lake_room as lake_room
import room
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    course_sand = lake_room.LakeRoom_underwater('course sand', roomPath, 'domains.school.elementQuest.lake_ne')
    course_sand.set_description('course sand', 'Here, the bottom of the lake is empty, except for a coating of course sand.')
    course_sand.add_exit('west', 'domains.school.elementQuest.oysters')
    course_sand.add_exit('south', 'domains.school.elementQuest.doorway')
    
    return course_sand
