import room
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    bedroom = Room('bedroom', pref_id='br31795')
    bedroom.set_description('normal bedroom', 'This bedroom is small but nice. There are bookshelves on the walls and a great big window overlooking Firlefile sorcery school. ')
    bedroom.add_exit('down', 'home.alex.house.lr31795')
    bedroom.add_adjectives('small', 'comfortable')

    bed = gametools.clone('home.alex.house.bed')
    bed.move_to(bedroom, True)
    return bedroom
