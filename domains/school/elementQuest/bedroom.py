import room
import gametools
import scenery
import doors_and_windows

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = room.Room('bedroom', roomPath, indoor=True)
    r.set_description('small bedroom', 'You find yourself in a small bedroom with stone walls and a giant window. '
    'A large bed stands in the centre of the room, facing the window. Beside the window you see a glass door '
    'leading out onto a balcony. There is also a wooden door leading to the east and a ladder leading up.')
    r.add_exit('up', 'domains.school.elementQuest.study')

    east_door = doors_and_windows.Door('door', 'wooden door', 'This is a wooden door leading to the east.', 'domains.school.elementQuest.armor_museum', 'east')
    east_door.add_adjectives('wooden')
    r.insert(east_door)

    west_door = doors_and_windows.Door('door', 'glass door', 'This tinted glass door leads out onto a balcony.', 'domains.school.elementQuest.bedroom_balcony', 'west')
    west_door.add_adjectives('glass')
    r.insert(west_door)

    bed = gametools.clone('domains.school.elementQuest.bed')
    r.insert(bed)

    bedside_table = gametools.clone('domains.school.elementQuest.bedside_table')
    r.insert(bedside_table)

    return r
