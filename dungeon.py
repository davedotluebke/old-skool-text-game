from room import Room

lair = Room('lair')
crawlway = Room('crawlway')
dungon_hall = Room('dungon hall')
great_cavern = Room('cavern')
dead_end = Room('tunnel end')

lair.set_description('monster\'s lair', 'This is a lair where the terrible monster hides. It has a wall with clubs hanging on it. There is a crawlway to the northwest.')
crawlway.set_description('tight crawlway', 'This crawlway is a tight squeze, but you fit through. The monster would not, however.')
dungon_hall.set_description('dugeon hall', 'This is a old cave which has moss growing on the damp walls. It seems like it was made for a purpouse. There are tunnels to the north, south, and west, and a crawlway to the east.')
great_cavern.set_description('great cavern', 'This is a massive cavern, with a seat carved into the rocks on the west end. You can hardly see the roof, but it is dark in')

lair.add_exit('east', Thing.ID_dict['cave'])
lair.add_exit('northwest', crawlway)
crawlway.add_exit('southeast', lair)
crawlway.add_exit('north', dungon_hall)
dungon_hall.add_exit('east', crawlway)

lair.add_adjectives("monster's'")
crawlway.add_adjectives('tight')
dungon_hall.add_names('cave', 'dungon', 'hall')
dungon_hall.add_adjectives('purposefull')

crawlway.set_max_volume_carried(70)
