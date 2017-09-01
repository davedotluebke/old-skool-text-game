import gametools
import room
import domains.school.master_goblin as mod

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    root_room = room.Room('roots', roomPath)
    root_room.indoor = True
    root_room.set_description('crude dungeon', 'This is a crude dungeon with a shaft of light coming throgh some tree roots in a corner.')

    roots = gametools.clone('domains.school.dungeon.roots')
    root_room.insert(roots)
    return root_room
