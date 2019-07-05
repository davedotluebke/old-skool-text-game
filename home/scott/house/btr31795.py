import room
import gametools
import scenery

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    bathroom = room.Room('bathroom', pref_id=roomPath, indoor=True)
    bathroom.set_description('modern bathroom', 'This small bathroom has a bathtub, a shower, and a sink.')
    bathroom.add_exit('east', 'home.scott.house.lr31795')
    bathroom.add_adjectives('modern')

    bathtub = gametools.clone('home.scott.house.bathtub')
    bathtub.move_to(bathroom, True)

    sink = gametools.clone('home.scott.house.sink')
    sink.move_to(bathroom, True)

    toilet = scenery.Scenery('toilet', 'ordinary toilet', 'This is an ordinary toilet.')
    toilet.add_response(['flush'], 'You flush the toilet.')
    toilet.move_to(bathroom, True)

    cabinet = gametools.clone('home.scott.house.cabinets')
    cabinet.move_to(bathroom, True)

    return bathroom
