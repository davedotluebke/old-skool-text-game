import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('cavern', roomPath)
    r.set_description('tall cavern','You enter a tall cavern, with seemingly endless layers of balcony-like overlooks.')
    r.add_exit('east', 'domains.centrata.firefile_area.key_quest.maze3')

    giant = gametools.clone('domains.centrata.firefile_area.key_quest.giant')
    r.insert(giant)
    return r
