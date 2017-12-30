import room
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    bedroom = Room('bedroom', pref_id='br31795')
    bedroom.set_description('normal bedroom', 'This bedroom is small but nice. There are bookshelves on the walls and a great big window overlooking Firlefile sorcery school. ')
    bedroom.add_exit('down', living_room.id)
    bedroom.add_adjectives('small', 'comfortable')
    return bedroom
