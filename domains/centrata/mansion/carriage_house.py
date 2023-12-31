import gametools
import scenery
import keyed_door
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('house', roomPath, indoor=True)
    r.set_description('carriage house', 'You stand inside a large carriage house. The floor is tiled with stone tiles, and the walls are made of sandstone. There is a door to the west.')

    tile_floor = scenery.Scenery('floor', 'tile floor', 'This floor is tiled with stone tiles. They seem to form an irregular pattern.', unlisted=True)
    tile_floor.add_adjectives('tile', 'irregular')
    tile_floor.add_response(['remove', 'move'], 'The tiles seem firmly fastened to the floor.')
    r.insert(tile_floor, True)

    carriage_door = keyed_door.KeyedDoor('door', 'carriage door', 'This carriage door leads from the west lawn into the carriage house.', 'domains.centrata.mansion.west_lawn', 'north', 'domains.centrata.mansion.gate_key')
    carriage_door.add_adjectives('carriage')

    r.insert(carriage_door, True)

    return r
