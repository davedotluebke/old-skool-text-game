import room
import gametools
import home.scott.house.exit_door as exit_door

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    bedroom = room.Room('bedroom', pref_id=roomPath, indoor=True, safe=True)
    bedroom.set_description('circular bedroom', 'This small circular bedroom is built in the top of a tower. '
    'It has four large windows: one to the north, one to the south, one to the east, and one to the west.'
    'Strangely, each of the windows appears to look out on extremely different locations.')
    bedroom.add_exit('down', 'home.scott.house.lr31795')
    bedroom.add_adjectives('circular', 'windowed')

    north_window = exit_door.Window('window', 'northern window', 'This large window on the north side of the room has an almost invisible frame.', 'domains.school.forest.waterfall')
    north_window.add_adjectives('large', 'north')
    bedroom.insert(north_window, True)

    south_window = exit_door.Window('window', 'southern window', 'This large window on the south side of the room has an almost invisible frame.', 'domains.school.forest.waterfall')
    south_window.add_adjectives('large', 'south')
    bedroom.insert(south_window, True)

    bed = gametools.clone('home.scott.house.bed')
    bed.move_to(bedroom, True)
    return bedroom
