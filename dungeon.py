from thing import Thing
from room import Room
from scenery import Scenery

lair = Room('lair')
crawlway = Room('crawlway')
dungeon_hall = Room('dungeon hall')
great_cavern = Room('cavern')
dead_end = Room('tunnel end')

lair.set_description('monster\'s lair', 'This is a lair where the terrible monster hides. It has a wall with clubs hanging on it. There is a crawlway to the northwest.')
crawlway.set_description('tight crawlway', 'This crawlway is a tight squeze, but you fit through. The monster would not, however.')
dungeon_hall.set_description('dungeon hall', 'This is a old cave which has moss growing on the damp walls. It seems like it was made for a purpouse. There are tunnels to the north, south, and west, and a crawlway to the east.')
great_cavern.set_description('great cavern', 'This is a massive cavern, with a seat carved into the rocks on the west end. You can hardly see the roof, but it is letting a tiny bit of light in.')
dead_end.set_description('curved tunel cutoff', 'This is a curved end to a tunnel, which is very rocky and unclear, however, going on would involve tunnelling through rocks.')

lair.add_exit('east', Thing.ID_dict['cave'])
lair.add_exit('northwest', crawlway)
crawlway.add_exit('southeast', lair)
crawlway.add_exit('north', dungeon_hall)
great_cavern.add_exit('east', dungeon_hall)
dungeon_hall.add_exit('east', crawlway)
dungeon_hall.add_exit('west', great_cavern)
dungeon_hall.add_exit('south', dead_end)
dead_end.add_exit('north', dungeon_hall)

lair.add_adjectives("monster's'")
crawlway.add_adjectives('tight')
dungeon_hall.add_names('cave', 'dungeon', 'hall')
dungeon_hall.add_adjectives('purposefull')
dead_end.add_names('end')
dead_end.add_adjectives('dead', 'tunnel')

crawlway.set_max_volume_carried(70)

scroll = Scenery('scroll', 'scroll', 'This scroll appears to say something on it.')
scroll.add_adjectives('second')     #TODO: Identical object handeling
scroll.unfix()
scroll.add_response(['read'], "On the scroll there are theese words:\nFind thyself a power inside\nTake the a large stride\nBe the one who does not cower\nAnd be the one who discovers the power\n\nFinish your task to find the power\nHere upon ticks your hour...\n\n")
scroll.move_to(dungeon_hall)
