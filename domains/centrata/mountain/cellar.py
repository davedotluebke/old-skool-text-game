import gametools
import doors_and_windows
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    cellar = room.Room('cellar', roomPath, light=0)
    cellar.set_description('cold cellar', 'This cold cellar has an uneven floor. Several wooden shelves are fastened to the walls.')
    
    trapdoor = doors_and_windows.Door("trapdoor", "trapdoor in the floor", "This heavy wooden trapdoor is in the ceiling of the cellar", "domains.centrata.mountain.hut", "up", [])
    cellar.insert(trapdoor, True)
    
    cellar.add_exit('up', 'domains.centrata.mountain.hut')

    shelving = gametools.clone('domains.centrata.mountain.cellar_shelving')
    cellar.insert(shelving, True)

    return cellar
