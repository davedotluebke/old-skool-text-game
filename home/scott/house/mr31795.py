import gametools
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    magic_room = room.Room('magical room', roomPath, indoor=True)
    magic_room.set_description('magical room', 'This room has a lot of magical supplies. It also has a door on the west side of the room with a piece of paper above it.')
    magic_room.add_exit('north', 'home.scott.house.lr31795')
    magic_room.add_exit('west', 'domains.school.school.water_kitchen')
    magic_room.add_names('room')
    magic_room.add_adjectives('magic', 'magical')

    paper = gametools.clone('home.scott.house.placeChooser')
    magic_room.insert(paper, True)

    emerald = gametools.clone('home.scott.house.emerald')
    magic_room.insert(emerald, True)

    ruby = gametools.clone('home.scott.house.ruby')
    magic_room.insert(ruby, True)

    opal = gametools.clone('home.scott.house.opal')
    magic_room.insert(opal, True)
    
    return magic_room
