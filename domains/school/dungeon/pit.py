import gametools
import room
import domains.school.master_goblin as mod

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    pit = mod.PitRoom('pit', roomPath)
    return pit
