import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    hut = room.Room('hut', roomPath)
    hut.set_description('stone hut', 'Between the solid stone walls this small hut is dim and dark. A shaft of light enters the hut from a small hole in the thatched roof.')
    hut.add_exit('south', 'domains.centrata.mountain.peak')
    
    rug = gametools.clone('domains.centrata.mountain.rug')
    hut.insert(rug, True)

    hut.passage_revealed = False

    return hut
