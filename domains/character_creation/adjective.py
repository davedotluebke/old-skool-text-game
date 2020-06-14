import room
import gametools
import domains.character_creation.mirror as mirror
import domains.character_creation.plaque as plaque

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = room.Room('adjective_room', roomPath)
    r.set_description('boundless room', 'You find yourself in a room with a glass floor and walls. '
        'You see one mirror, with a plaque above it.')

    mirror_obj = mirror.Mirror('shimmering','a reflection of the plaque above',gametools.DEFAULT_START_LOC)
    r.insert(mirror_obj)

    plaque_obj = plaque.Plaque(mirror_obj, 1)
    r.insert(plaque_obj)
    
    return r
