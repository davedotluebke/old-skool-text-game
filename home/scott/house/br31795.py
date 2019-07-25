import room
import gametools
import home.scott.house.exit_door as exit_door

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    bedroom = room.Room('bedroom', pref_id=roomPath, indoor=True, safe=True)
    bedroom.set_description('normal bedroom', 'This bedroom is small but nice. There are bookshelves on the walls and a great big window overlooking Firlefile sorcery school. ')
    bedroom.add_exit('down', 'home.scott.house.lr31795')
    bedroom.add_adjectives('small', 'comfortable')

    window = exit_door.Window('window', 'large window', 'This large window has an almost invisible frame.', 'domains.school.forest.waterfall')
    window.add_adjectives('large')
    bedroom.insert(window, True)

    bed = gametools.clone('home.scott.house.bed')
    bed.move_to(bedroom, True)
    return bedroom
