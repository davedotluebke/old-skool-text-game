import gametools
import scenery
import room
import doors_and_windows

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    peak = room.Room('peak', roomPath)
    peak.set_description('rocky peak', 'This rocky peak overlooks a mountain range to the west. On the north end of the rocks there is a small hut.')
    peak.add_exit('east', 'domains.centrata.mountain.clifftop')

    hut = scenery.Scenery("hut", "stone hut", "This small stone hut stands alone atop the peak of the mountain. It looks weathered, as if it has not seen use in many years. A small open doorway leads inside.", unlisted=True)
    peak.insert(hut, True)

    hut_doorway = doors_and_windows.Door("doorway", "doorway", "This stone doorway leads into the hut.", "domains.centrata.moutain.hut", "north", [])
    hut_doorway.add_adjectives("stone")
    hut_doorway.open_door_fc()
    peak.insert(hut_doorway, True)
    
    return peak
