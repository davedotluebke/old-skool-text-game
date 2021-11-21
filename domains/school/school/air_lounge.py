import room
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    air_lounge = room.Room('lounge', roomPath, safe=True)
    air_lounge.set_description()