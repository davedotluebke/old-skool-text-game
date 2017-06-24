from room import Room
from thing import Thing
from owen_domain import PlaceChooser

waterfall = Room('waterfall')
waterfall.set_description('beutiful waterfall base', 'This is a beutiful waterfall base. From here you can stand and look at the rushing waterfall. This place makes you feel peaceful inside, and happy. You will always remember this place.')
waterfall.add_adjectives('waterfall', 'beutiful', 'special')
waterfall.add_names('place', 'base')
waterfall.add_exit('west', Thing.ID_dict['woods'])

paper = PlaceChooser('magic paper', 'trunk of a tree')
paper.move_to(waterfall)
