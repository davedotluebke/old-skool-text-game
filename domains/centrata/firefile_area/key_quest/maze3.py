import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('passage', roomPath, indoor=True)
    r.set_description('shafted passage','This passage is brigher than the others due to a shaft of light coming from the ceiling. You see some stalagtites you think you might be able to climb.')
    r.add_exit('east', 'domains.centrata.firefile_area.key_quest.maze27')
    r.add_exit('west', 'domains.centrata.firefile_area.key_quest.maze4')

    stalagtites = scenery.Scenery('stalagtites', 'stalagtites', 'These stalagtites look sturdy but slippery.')
    stalagtites.add_response(['climb'], 'Unfortunately, the stalagtites are too slipery to climb.')
    stalagtites.unlisted = True
    r.insert(stalagtites, True)

    return r
