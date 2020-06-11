import gametools
import room
import scenery
import doors_and_windows

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    lobby = room.Room('lobby', safe=True, indoor=True, pref_id=roomPath)
    lobby.set_description('small lobby', "This is a small lobby at the entrance to Renaissance School. "
    "To the south a wooden bench stands in front of a large window into a staircase. To the east a door "
    "leads into an office. To the west the room expands into the front offices of the school. To the north "
    "there is a door that exits the building.")
    lobby.add_exit('west', 'domains.renaissance_school.front_offices')

    mj_door = doors_and_windows.Door('door', 'plain white door', 'This plain white door is on the east side of the room. '
    'It has a label on it reading "Sara Johson, head of school".', 'domains.renaissance_school.mjs_office', 'east', 'everyone')
    mj_door.add_adjectives('plain', 'white', 'mj', 'mjs', 'mj\'s')
    mj_door.move_to(lobby, True)

    int_window = doors_and_windows.Window("window", "interior window", "This strange interior window is between the front lobby and the front stairwell. ", "domains.renaissance_school.front_stairwell")
    int_window.add_adjectives("interior")
    int_window.move_to(lobby, True)

    bench = scenery.Scenery('bench', 'wooden bench', 'This wooden bench is on the south side of the room. The back of it is made from raw branches.', unlisted=True)
    bench.add_adjectives('wooden', 'south')
    bench.add_response(['take'], 'The bench is too heavy and awkward to move.')
    bench.add_response(['sit'], 'You sit on the bench.')
    bench.add_response(['stand'], 'You stand up.', False, True)
    bench.move_to(lobby, True)

    flyer_box = gametools.clone('domains.renaissance_school.flyer_box')
    flyer_box.move_to(lobby, True)

    return lobby
