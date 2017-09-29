import room
import scenery
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    dark_forest = room.Room('darkforest' , roomPath)
    dark_forest.set_description('scary dark forest', 'This is a scary dark forest you want to leave. Soon!')
    dark_forest.add_exit("south", "domains.school.forest.forest3")
    dark_forest.add_exit("north", "domains.school.forest.gloomy_forest")

    dead_tree = scenery.Scenery('dead tree', 'big dead tree', 'This dead tree is big and bare with no bark. At the bottom of it there is a rat hole. ')
    dark_forest.insert(dead_tree)

    return dark_forest