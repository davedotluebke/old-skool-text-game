import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    cellar = room.Room('cellar', roomPath, light=0)
    cellar.set_description('cold cellar', 'This cold cellar has an uneven floor. Several wooden shelves are fastened to the walls.')
    cellar.add_exit('up', 'domains.centrata.mountain.hut')

    shelving = gametools.clone('domains.centrata.mountain.cellar_shelving')
    cellar.insert(shelving, True)

    return cellar
