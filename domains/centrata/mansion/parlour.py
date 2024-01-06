import gametools
import scenery
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('parlour', roomPath, indoor=True)
    r.set_description('well-furnished parlour', 'You step into a well-furnished parlour, complete with several sofas and armchairs. The wallpaper is a dark red, pairing with the green of the furniture. Passages lead south and northwest, while there are doors to the north and the southwest.')
    r.add_exit('south', 'domains.centrata.mansion.office')

    # TODO: Add more scenery

    return r
