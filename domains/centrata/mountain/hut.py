import gametools
import scenery
import room
import doors_and_windows

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    hut = room.Room('hut', roomPath)
    hut.set_description('stone hut', 'Between the solid stone walls this small hut is dim and dark. A shaft of light enters the hut from a small hole in the thatched roof.')
    hut.add_exit('south', 'domains.centrata.mountain.peak')
    
    rug = gametools.clone('domains.centrata.mountain.rug')
    hut.insert(rug, True)

    hole = scenery.Scenery("hole", "hole in roof", "This hole in the roof looks as if it was placed intentionally, to vent a fire.")
    hut.insert(hole, True)

    hut_doorway = doors_and_windows.Door("doorway", "doorway", "This stone doorway leads out of the hut.", "domains.centrata.moutain.peak", "south", [])
    hut_doorway.add_adjectives("stone")
    hut.insert(hut_doorway, True)

    hut.passage_revealed = False

    return hut
