import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    peak = room.Room('peak', roomPath)
    peak.set_description('rocky peak', 'This rocky peak overlooks a mountain range to the west. On the north end of the rocks there is a small hut.')
    peak.add_exit('east', 'domains.centrata.mountain.clifftop')
    peak.add_exit('north', 'domains.centrata.mountain.hut')

    hut = scenery.Scenery("hut", "stone hut", "This small stone hut stands alone atop the peak of the mountain. It looks weathered, as if it has not seen use in many years. A small open doorway leads inside.", unlisted=True)
    peak.insert(hut, True)
    
    return peak
