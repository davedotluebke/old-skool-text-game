import gametools
import scenery
import room
import keyholemod

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('passage', roomPath)
    r.set_description('dark passage','This is a dark and steep passage. Light flows in through a keyhole-shaped carving in the rock to the north.')
    r.add_exit('down', 'domains.centrata.firefile_area.key_quest.maze99')

    keyhole = keyholemod.Keyhole('north', 'domains.centrata.firefile_area.key_quest.maze_exit1', 2)
    keyhole.move_to(r, True)

    return r
