import gametools
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    dead_end = room.Room('tunnel end', roomPath)
    dead_end.indoor = True
    dead_end.set_description('curved tunnel cutoff', 'This is a curved end to a tunnel, which is very rocky and unclear. Going on would involve tunneling through rocks.')
    dead_end.add_exit('north', 'domains.school.dungeon.dungeon_hall')
    dead_end.add_names('end')
    dead_end.add_adjectives('dead', 'tunnel')
    return dead_end
