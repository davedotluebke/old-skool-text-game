def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    dark_forest = room.Room('darkforest' , roomPath)
    dark_forest.set_description('gloomy, gloomy forest', 'This is a goomly forest, it is misty and dim. You feel a slight unease.')
    dark_forest.add_exit("south", "domains.school.forest.forest3")
    dark_forest.add_exit("north", "domains.school.forest.gloomy_forest")


    dead_tree = scenery.Scenery('haunted_tree', 'dark tree', 'This tree seemes to swing even though there is no wind and you think youmight be able to make out a shadowy figure high in the branches.')
    dead_tree.add_names('tree')
    dead_tree.add_adjectives('dead')
    dead_tree.add_response(['climb'], 'When you try to climb the tree, the branch you grab on to breaks off with an eerie snap.')
    dark_forest.insert(dead_tree)