import gametools
import room
import doors_and_windows

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    living_room = room.Room('living room', pref_id=roomPath, indoor=True, safe=True)
    living_room.set_description('well-kept living room', 'This is a comfortable living room, while quite small. '
    'It has a couch on one wall. You see doors to the east and west, open doorways to the north and south,'
    ' and a large window to the southeast.')
    living_room.add_exit('up', 'home.johanna.house.br31795')
    living_room.add_exit('south', 'home.johanna.house.mr31795')
    living_room.add_exit('north', 'home.johanna.house.er31795')
    living_room.add_names('room', 'space')
    living_room.add_adjectives('living', 'well-kept', 'comfortable')

    d = doors_and_windows.Door('door', 'strong birch door', 'This is a strong birch door on the east side of the room.', 'domains.school.school.hallway', 'east', ['johanna'])
    d.add_adjectives('birch')
    d.move_to(living_room, True)

    bath_door = doors_and_windows.Door('door', 'plain interior door', 'This is a plain interior door on the west side of the room.', 'home.johanna.house.btr31795', 'west', ['johanna'])
    bath_door.add_adjectives('plain', 'interior', 'bathroom')
    bath_door.move_to(living_room, True)

    w = doors_and_windows.Window('window', 'large window', 'This is a very large window looking over the great hall.', 'domains.school.school.great_hall')
    w.add_adjectives('large')
    w.move_to(living_room, True)

    bookshelf = gametools.clone('home.johanna.house.bookshelf')
    bookshelf.move_to(living_room, True)

    couch = gametools.clone('home.johanna.house.couch')
    couch.move_to(living_room, True)

    return living_room
