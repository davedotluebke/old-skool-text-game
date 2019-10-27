import gametools
import room
import home.scott.house.exit_door as exit_door

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    living_room = room.Room('living room', pref_id=roomPath, indoor=True, safe=True)
    living_room.set_description('well-kept living room', 'This is a comfortable living room, while quite small. It has a couch on one wall. You see a door to the east and a large window to the southeast.')
    living_room.add_exit('west', 'home.scott.house.btr31795')
    living_room.add_exit('up', 'home.scott.house.br31795')
    living_room.add_exit('south', 'home.scott.house.mr31795')
    living_room.add_exit('north', 'home.scott.house.er31795')
    living_room.add_names('room', 'space')
    living_room.add_adjectives('living', 'well-kept', 'comfortable')

    d = exit_door.Door('door', 'strong birch door', 'This is a strong birch door on the east side of the room.', 'domains.school.school.hallway', 'east')
    d.add_adjectives('birch')
    d.move_to(living_room, True)

    w = exit_door.Window('window', 'large window', 'This is a very large window looking over the great hall.', 'domains.school.school.great_hall')
    w.add_adjectives('large')
    w.move_to(living_room, True)

    bookshelf = gametools.clone('home.scott.house.bookshelf')
    bookshelf.move_to(living_room, True)

    couch = gametools.clone('home.scott.house.couch')
    couch.move_to(living_room, True)

    return living_room
