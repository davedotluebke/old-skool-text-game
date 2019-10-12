import gametools
import scenery
import room
import domains.centrata.firefile_area.key_quest.keyholemod as k

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('passage', roomPath, indoor=True)
    r.set_description('dark passage','This is a dark and steep passage. Light flows in through a keyhole-shaped carving in the rock to the north.')
    r.add_exit('down', 'domains.centrata.firefile_area.key_quest.maze99')

    keyhole = k.Keyhole('north', 'domains.centrata.firefile_area.key_quest.exit1', 2)
    keyhole.move_to(r, True)

    key = gametools.clone('domains.centrata.firefile_area.key_quest.key')
    key.qkey_number = 3
    key.move_to(r, True)

    return r
