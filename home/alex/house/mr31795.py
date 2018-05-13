import gametools
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    magic_room = room.Room('magical room', roomPath, indoor=True)
    magic_room.set_description('magical room', 'This room has a lot of magical supplies. It also has a door on the west side of the room with a piece of paper above it.')
    magic_room.add_exit('north', 'home.alex.house.lr31795')
    magic_room.add_exit('west', 'woods')
    magic_room.add_names('room')
    magic_room.add_adjectives('magic', 'magical')

    paper = gametools.clone('home.alex.house.paper')
    magic_room.insert(paper, True)
    return magic_room
