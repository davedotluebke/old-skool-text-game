from thing import Thing
from room import Room
from scenery import Scenery
from trapthings import TrapThing

lair = Room('lair')
crawlway = Room('crawlway')
dungeon_hall = Room('dungeon hall', pref_id='scrollchangeroom1')
great_cavern = Room('cavern')
dead_end = Room('tunnel end')
small_tunnel = Room('tunnel')
trap = Room('gold room', pref_id='trap')

lair.set_description('monster\'s lair', 'This is a lair where the terrible monster hides. It has a wall with clubs hanging on it. There is a crawlway to the northwest.')
crawlway.set_description('tight crawlway', 'This crawlway is a tight squeze, but you fit through. The monster would not, however.')
dungeon_hall.set_description('dungeon hall', 'This is a old cave which has moss growing on the damp walls. It seems like it was made for a purpouse. There are tunnels to the north, south, and west, and a crawlway to the east.')
great_cavern.set_description('great cavern', 'This is a massive cavern, with a seat carved into the rocks on the west end. You can hardly see the roof, but it is letting a tiny bit of light in.')
dead_end.set_description('curved tunel cutoff', 'This is a curved end to a tunnel, which is very rocky and unclear, however, going on would involve tunnelling through rocks.')
small_tunnel.set_description('small tunnel', 'You are in a small tunnel, which turns into a crawlway to the south. There is an exit off the tunnel to the west whcih has a yellow glow comming from the end. A dark tunnel leads north.')
trap.set_description('room with gold in the center', 'You are in a large room. In the center of the room is a big pile of gold coins.')

lair.add_exit('east', Thing.ID_dict['cave'])
lair.add_exit('northwest', crawlway)
crawlway.add_exit('southeast', lair)
crawlway.add_exit('north', dungeon_hall)
great_cavern.add_exit('east', dungeon_hall)
great_cavern.add_exit('southwest', small_tunnel)
dungeon_hall.add_exit('east', crawlway)
dungeon_hall.add_exit('west', great_cavern)
dungeon_hall.add_exit('south', dead_end)
dead_end.add_exit('north', dungeon_hall)
small_tunnel.add_exit('northeast', great_cavern)
small_tunnel.add_exit('west', trap)
trap.add_exit('east', small_tunnel)

lair.add_adjectives("monster's")
crawlway.add_adjectives('tight')
dungeon_hall.add_names('cave', 'dungeon', 'hall')
dungeon_hall.add_adjectives('purposefull')
dead_end.add_names('end')
dead_end.add_adjectives('dead', 'tunnel')
small_tunnel.add_adjectives('small')
trap.add_names('room', 'trap')
trap.add_adjectives('gold')

crawlway.set_max_volume_carried(70)

gold = TrapThing('gold', 'You try to take the gold but a trap is sprung! You fall into a great void...', Thing.ID_dict['nulspace'], 'goldtrap9125')
gold.set_description('bunch of shiny gold coins', 'This is a collection of 50 shiny real gold coins.')
gold.set_weight(74000)
gold.move_to(trap)
