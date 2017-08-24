import gametools
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    dead_end = room.Room('tunnel end', roomPath)
    dead_end.set_description('curved tunel cutoff', 'This is a curved end to a tunnel, which is very rocky and unclear, however, going on would involve tunnelling through rocks.')
    dead_end.add_exit('north', 'domains.school.dungeon.dungeon_hall')
    dead_end.add_names('end')
    dead_end.add_adjectives('dead', 'tunnel')
    return dead_end
