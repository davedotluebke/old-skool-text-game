import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('cavern', roomPath, indoor=True)
    r.set_description('tall cavern','You enter a tall cavern, with seemingly endless layers of balcony-like overlooks. You notice a huge slab of flowstone to the east.')
    r.add_exit('east', 'domains.centrata.key_quest.maze3')

    flowstone = scenery.Scenery('flowstone', 'huge slab of flowstone', 'This slab of flowstone is huge and looks as if it is a waterfall frozen in motion.')
    flowstone.unlisted = True
    flowstone.add_adjectives('huge', 'wet')
    flowstone.add_response(['climb', 'traverse'], "You try to climb the slab but can't find any good holds on it.")
    flowstone.move_to(r, True)

    giant = gametools.clone('domains.centrata.key_quest.giant')
    r.insert(giant)
    
    return r
