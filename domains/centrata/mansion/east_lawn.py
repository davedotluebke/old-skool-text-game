import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('lawn', roomPath)
    r.set_description('east lawn', 'You stand outside the mansion on the east side.')
    r.add_exit('northwest', 'domains.centrata.mansion.gate_inside')
    r.add_exit('southwest', 'domains.centrata.mansion.south_lawn')

    mansion_scenery_east = scenery.Scenery('mansion', 'sandstone mansion', 'A massive bay window looks out onto the lawn. A wing stretches out to the south.', unlisted=True)
    mansion_scenery_east.add_adjectives('sandstone', 'massive')
    r.insert(mansion_scenery_east, True)

    bay_window_scenery = scenery.Scenery('window', 'bay window', 'This massive bay window looks out over the lawn. However, it\'s too dark inside to see in.')
    bay_window_scenery.add_adjectives('bay', 'massive')
    bay_window_scenery.add_response(['climb'], 'This bay window is too high off the ground to easily climb through.')
    r.insert(bay_window_scenery, True)

    return r
