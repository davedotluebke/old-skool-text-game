import room
import gametools
import scenery
import doors_and_windows

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    bathroom = room.Room('bathroom', pref_id=roomPath, indoor=True, safe=True)
    bathroom.set_description('modern bathroom', 'This small bathroom has a bathtub, a shower, and a sink. There is a door on the east side of the room.')
    bathroom.add_adjectives('modern')

    bath_door = doors_and_windows.Door('door', 'plain interior door', 'This is a plain interior door on the east side of the room.', 'home.johanna.house.lr31795', 'east', 'everyone')
    bath_door.add_adjectives('plain', 'interior', 'bathroom')
    bath_door.move_to(bathroom, True)

    bathtub = gametools.clone('home.johanna.house.bathtub')
    bathtub.move_to(bathroom, True)

    sink = gametools.clone('home.johanna.house.sink')
    sink.move_to(bathroom, True)

    toilet = scenery.Scenery('toilet', 'ordinary toilet', 'This is an ordinary toilet.')
    toilet.add_response(['flush'], 'You flush the toilet.')
    toilet.move_to(bathroom, True)

    cabinet = gametools.clone('home.johanna.house.cabinets')
    cabinet.move_to(bathroom, True)

    return bathroom
