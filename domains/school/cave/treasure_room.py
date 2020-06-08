import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('cave', roomPath, indoor=True)
    r.set_description('large cave','This is a large cave with an opening in the ceiling. You see some stalagtites you think you might be able to climb.')
    r.add_exit('southeast', 'domains.school.cave.lair')

    stalagtites = scenery.Scenery('stalagtites', 'stalagtites', 'These stalagtites look sturdy but slippery.')
    stalagtites.add_response(['climb'], 'Unfortunately, the stalagtites are too slipery to climb.')
    stalagtites.unlisted = True
    r.insert(stalagtites, True)

    gold = gametools.clone('currencies.gold')
    gold.plurality = 100
    r.insert(gold, True)

    return r
