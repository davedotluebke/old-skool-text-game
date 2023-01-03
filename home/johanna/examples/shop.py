import gametools
import scenery
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = room.Room('shop', roomPath, safe=True, indoor=True)
    r.set_description('shop', 'You enter a shop full of various items, all for sale.')

    shopkeeper = gametools.clone('home.johanna.examples.shopkeeper')
    shopkeeper.move_to(r)

    return r
