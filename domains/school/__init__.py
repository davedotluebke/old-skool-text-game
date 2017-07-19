# This code initializes the school directory. Having this file makes python treat this directory as a submodule.
from thing import Thing

#import domains.school.forest
import domains.school.farfile
#import domains.school.waterfall
#import domains.school.cave
#import domains.school.dungeon

#adding a few connections
#cave.cave_entrance.add_aditional_vars(forest.forest_three.id, Thing.ID_dict['nulspace'].game)
#cave.cave.add_exit('east', forest.forest_three.id)
#cave.cave_entrance.add_exit('east', forest.forest_three.id)
#Thing.ID_dict['nulspace'].game.register_heartbeat(cave.cave)
#dungeon.crawlway.add_exit('southeast', cave.lair.id)
#forest.forest_three.add_exit('west', cave.cave_entrance.id)
