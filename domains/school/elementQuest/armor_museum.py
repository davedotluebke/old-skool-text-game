import room
import gametools
import scenery
import doors_and_windows

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('museum', roomPath, indoor=True)
    r.set_description('armor museum', 'You find yourself in a stone tower that has clearly been turned into an armor museum. '
    'Three large glass cases with armor are in the room. In the centre of the room you see a table covered with a large coat '
    'of arms. There is a door to the west, a doorway to the east, and a wooden staircase leading up and down.')
    r.add_adjectives('armor', 'tower')
    r.add_exit('east', 'domains.school.elementQuest.armoury')
    r.add_exit('down', 'domains.school.elementQuest.portrait_gallery')
    r.add_exit('up', 'domains.school.elementQuest.living_space')

    armor_case_one = scenery.Scenery('case', 'glass case', 'This glass case surrounds a suit of plate armor.', unlisted=True)
    armor_case_one.add_adjectives('armor', 'armour', 'glass')
    armor_case_one.add_response(['take', 'get'], 'The glass case is built into the room.')
    armor_case_one.add_response(['open'], 'The case is locked.')
    armor_case_one.add_response(['unlock'], 'You don\'t have the key.')
    armor_case_one.add_response(['break', 'destroy', 'force'], 'Despite your best effort, you cannot break the glass case.')
    armor_case_one.add_response(['close', 'shut'], 'The case is already closed!')
    r.insert(armor_case_one)

    armor_case_two = scenery.Scenery('case', 'glass case', 'This glass case surrounds a suit of chain mail.', unlisted=True)
    armor_case_two.add_adjectives('armor', 'armour', 'glass')
    armor_case_two.add_response(['take', 'get'], 'The glass case is built into the room.')
    armor_case_two.add_response(['open'], 'The case is locked.')
    armor_case_two.add_response(['unlock'], 'You don\'t have the key.')
    armor_case_two.add_response(['break', 'destroy', 'force'], 'Despite your best effort, you cannot break the glass case.')
    armor_case_two.add_response(['close', 'shut'], 'The case is already closed!')
    r.insert(armor_case_two)
    
    armor_case_three = scenery.Scenery('case', 'glass case', 'This glass case surrounds a suit of plate armor.', unlisted=True)
    armor_case_three.add_adjectives('armor', 'armour', 'glass')
    armor_case_three.add_response(['take', 'get'], 'The glass case is built into the room.')
    armor_case_three.add_response(['open'], 'The case is locked.')
    armor_case_three.add_response(['unlock'], 'You don\'t have the key.')
    armor_case_three.add_response(['break', 'destroy', 'force'], 'Despite your best effort, you cannot break the glass case.')
    armor_case_three.add_response(['close', 'shut'], 'The case is already closed!')
    r.insert(armor_case_three)

    armor_one = scenery.Scenery('armor', 'metal armor', 'This armor seems to be made of a heavy metal plate.', unlisted=True)
    armor_one.add_adjectives('metal', 'plate')
    armor_one.add_names('armour')
    armor_one.add_response(['take', 'get', 'wear', 'destroy', 'break', 'steal'], 'The armor is behind a glass case.')
    r.insert(armor_one)
    
    armor_two = scenery.Scenery('mail', 'chain mail', 'This chain mail looks sturdy but flexible.', unlisted=True)
    armor_two.add_adjectives('metal', 'plate')
    armor_two.add_names('armor', 'armour')
    armor_two.add_response(['take', 'get', 'wear', 'destroy', 'break', 'steal'], 'The armor is behind a glass case.')
    r.insert(armor_two)

    armor_three = scenery.Scenery('armor', 'metal armor', 'This armor seems to be made of a heavy metal plate.', unlisted=True)
    armor_three.add_adjectives('metal', 'plate')
    armor_three.add_names('armour')
    armor_three.add_response(['take', 'get', 'wear', 'destroy', 'break', 'steal'], 'The armor is behind a glass case.')
    r.insert(armor_three)

    table = gametools.clone('domains.school.elementQuest.arms_table')
    r.insert(table)

    west_door = doors_and_windows.Door('door', 'wooden door', 'This antique wooden door leads to the west.', 'domains.school.elementQuest.bedroom','west')
    west_door.add_adjectives('wooden', 'antique')
    west_door.open_door_fc()
    r.insert(west_door)

    return r
