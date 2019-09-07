import room
import scenery
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    dark_forest = room.Room('darkforest' , roomPath)
    dark_forest.set_description('scary, dark forest', 'This is a scary, dark forest that you want to leave...soon!')
    dark_forest.add_exit("south", "domains.school.forest.forest3")
    dark_forest.add_exit("north", "domains.school.forest.gloomy_forest")

    dead_tree = scenery.Scenery('dead_tree', 'big dead tree', 'This dead tree is big and bare with no bark. At the bottom of it there is a rat hole. ')
    dead_tree.add_names('tree')
    dead_tree.add_adjectives('dead')
    dead_tree.add_response(['climb'], 'When you try to climb the tree, the branch you grab on to breaks off with an eerie snap.')
    dark_forest.insert(dead_tree)

    rat = gametools.clone('domains.school.forest.rat')
    rat.move_to(dark_forest)

    return dark_forest