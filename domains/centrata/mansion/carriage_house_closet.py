import gametools
import scenery
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('closet', roomPath, indoor=True)
    r.set_description('carriage house closet', 'You find yourself in a large closet, filled to the brim with supplies.')
    r.add_exit('east', 'domains.centrata.mansion.carriage_house')

    tile_floor = scenery.Scenery('floor', 'tile floor', 'This floor is tiled with stone tiles. They seem to form an irregular pattern.', unlisted=True)
    tile_floor.add_adjectives('tile', 'irregular')
    tile_floor.add_response(['remove', 'move'], 'The tiles seem firmly fastened to the floor.')
    r.insert(tile_floor, True)

    ladder = gametools.clone('domains.centrata.mansion.ladder')
    r.insert(ladder, True)

    rake = gametools.clone('domains.centrata.mansion.rake')
    hoe = gametools.clone('domains.centrata.mansion.hoe')
    bucket = gametools.clone('domains.centrata.mansion.bucket')
    shovel = gametools.clone('domains.centrata.mansion.shovel')

    r.insert(rake, True)
    r.insert(hoe, True)
    r.insert(bucket, True)
    r.insert(shovel, True)

    return r
