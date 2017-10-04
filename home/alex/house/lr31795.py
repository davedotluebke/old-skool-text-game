import gametools
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    living_room = Room('living room', pref_id=roomPath)
    living_room.set_description('well-kept living room', 'This is a comfortable living room, while quite small. It has a couch on one wall.')
    living_room.add_exit('west', 'home.alex.house.btr31795')
    living_room.add_exit('up', 'home.alex.house.br31795')
    living_room.add_exit('south', 'home.alex.house.mr31795')
    living_room.add_names('room', 'space')
    living_room.add_adjectives('living', 'well-kept', 'comfortable')
