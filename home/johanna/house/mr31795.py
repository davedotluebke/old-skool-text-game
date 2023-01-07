import gametools
import room
import doors_and_windows

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    magic_room = room.Room('magical room', roomPath, indoor=True)
    magic_room.set_description('magical room', 'This room has a lot of magical supplies. It also has a door on the west side of the room with a piece of paper above it.')
    magic_room.add_exit('north', 'home.johanna.house.lr31795')
    magic_room.add_names('room')
    magic_room.add_adjectives('magic', 'magical')

    d = doors_and_windows.Door('door', 'strong osmium door', 'This door is made of pure osmium. It is on the west side of the room.', 'domains.school.school.water_kitchen', 'west', ['johanna'])
    d.add_adjectives('osmium', 'magic')
    magic_room.insert(d, True)
    magic_room.west_door = d

    paper = gametools.clone('home.johanna.house.placeChooser')
    magic_room.insert(paper, True)

    emerald = gametools.clone('home.johanna.house.emerald')
    magic_room.insert(emerald, True)

    ruby = gametools.clone('home.johanna.house.ruby')
    magic_room.insert(ruby, True)

    opal = gametools.clone('home.johanna.house.opal')
    magic_room.insert(opal, True)

    diamond = gametools.clone('home.johanna.house.diamond')
    magic_room.insert(diamond, True)

    cauldron = gametools.clone('domains.school.school.cauldron')
    magic_room.insert(cauldron, True)
    
    return magic_room
