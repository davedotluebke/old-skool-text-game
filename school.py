from thing import Thing
from bookcase import Bookcase
from container import Container
from room import Room
from scenery import Scenery
from cauldron import Cauldron
from liquid import Liquid

from debug import dbg 

grand_entry = Room('grand entry', safe=True)
great_hall = Room('great hall', safe=True)
landing = Room('landing', safe=True)
gallery = Room('gallery', safe=True)
library = Room('library', safe=True)
hmasters_office = Room('office', safe=True)
towerstairs = Room('towerstairs', safe=True)
lookout = Room('lookout', safe=True)
potion_storage = Room('potion storage', safe=True)
hallway = Room('hallway', safe=True)

grand_entry.set_description('grand school entryway', 'This is the most magnificent entryway you have ever seen. The enormous front door is at the top of the marble staircase, with huge pillars on either side.')
great_hall.set_description('Great Hall', 'This is the biggest room in the entire school, and it is enormous. It is made of ancient stones. To the east a grand staircase rises to an elevated landing.')
landing.set_description('elevated landing overlooking the great hall', 'You stand on a landing of a grand staircase, overlooking the cavernous Great Hall. From here the staircase splits to two smaller staircases, to the northeast and southeast, which lead to the next level.')
gallery.set_description('portrait gallery', "This gradiose portrait gallery overlooks the Great Hall through a pillared colonade.")
library.set_description('library', "You find yourself in a comfortable library filled from floor to ceiling with books and bookcases. The room is circular, and must be built into a round tower as windows look out in every direction. A spiral staircase in the center of the room leads upwards.")
hmasters_office.set_description('grandiose headmasters office', 'You look at a giant room with a large bay window in the back. There is a giant carved oak desk in the middle of the room. There are many bookcases lining the walls, and stacks of papers on the desk.')
towerstairs.set_description('spiral staircase leading up the tower', 'You find yourself in a enormous tower, with winding stairs leading up it. There is a small door to the east.')
lookout.set_description('circular lookout', 'This lookout looks over the entire school and surrounding area. With 360 degree views, you see:'+  \
'\n'+'a thick forest \n'+'a little house \n'+'a garden \n'+'a distant mountain range \n'+'more thick forest, and some school grounds \n'+'even more forest that streaches on for hundreds of miles')
potion_storage.set_description('potion storage room', 'This is a stonewalled potion storage room, dimly lit. It has many cauldrons on a open shelf, and many burners for stirring cauldrons. It has many ingredients in a different open shelf across the room.'
'You have to step carefully here, as the floor is covered in shards of broken glass.')
hallway.set_description('staff office hallway', 'This hallway leads to all of the staff offices. It is very blank on the walls, however, the walls themselves are intricate and have little carved patterens in them.')

grand_entry.add_names('entry', 'entryway')
grand_entry.add_adjectives('grand', 'magnificent')
great_hall.add_names('hall', 'chamber')
great_hall.add_adjectives('grand', 'enourmous')
hmasters_office.add_adjectives("grandiose", 'headmaster\'s')
towerstairs.add_names('stairs')
towerstairs.add_adjectives('tower', 'spiral')
lookout.add_adjectives('circular')
potion_storage.add_names('potion', 'storage')
potion_storage.add_names('room')
hallway.add_adjectives('staff', 'office')

grand_entry.add_exit('southwest', Thing.ID_dict['field'])
grand_entry.add_exit('northwest', Thing.ID_dict['garden'])
grand_entry.add_exit('east', great_hall)
great_hall.add_exit('west', grand_entry)
great_hall.add_exit('east', landing)
landing.add_exit('northeast', gallery)
landing.add_exit('southeast', library)
landing.add_exit('west', great_hall)
gallery.add_exit('east', landing)
gallery.add_exit('north', hmasters_office)
gallery.add_exit('northeast', hallway)
library.add_exit('northwest', landing)
library.add_exit('up', towerstairs)
hmasters_office.add_exit('south', gallery)
towerstairs.add_exit('down', library)
towerstairs.add_exit('up', lookout)
lookout.add_exit('down', towerstairs)
potion_storage.add_exit('up', library)
hallway.add_exit('south', gallery)

bookcase = Bookcase('bookcase', potion_storage)
library.insert(bookcase)

b_table = Container('table')
b_table.set_description('banquet-size table', 'This is a extremely long banquet table, stretching almost from one end of the room to the other.')
b_table.fix_in_place('Moving this table would require a lot of help.')
b_table.add_adjectives('massive', 'enormous', 'long', 'banquet')
b_table.set_prepositions('on', "onto")
b_table.set_max_weight_carried(4e9)
b_table.set_max_volume_carried(3e9)
great_hall.insert(b_table)

desk = Container('desk')
desk.set_description('carved oak desk', 'This carved oak desk is clearly more than 100 years old, and is carved out in the shapes of dragons and other vicious creatures.')
desk.fix_in_place('The desk is very, very heavy, and feels rooted to the floor.')
desk.add_adjectives('carved', 'oak')
desk.set_prepositions('on', 'onto', 'in', 'into')
desk.set_max_weight_carried(4e9)
desk.set_max_volume_carried(80)
desk.move_to(hmasters_office)

cauldron = Cauldron('cauldron')
cauldron.set_description('iron cauldron', 'This is a iron cauldron.')
cauldron.set_max_weight_carried(2000)
cauldron.set_max_volume_carried(30)
cauldron.move_to(potion_storage)

water = Liquid('water', 'some normal water', 'This is some normal clear water.')
water.add_response(['drink'], 'You take a big drink of the water, and your thirst is quenched.')

molasses = Liquid('molasses')
molasses.set_description('thick brown molasses', 'This brownish liquid is sweet and thick. Not surprisingly, it is used in recipes as a sweetener and a thickener.')
molasses.add_adjectives('thick', 'brown', 'brown', 'brownish')
molasses.set_volume(0.040)
molasses.set_weight(40)

flask = Container('flask')
flask.set_description('small flask', 'This is a small flask of clear glass. ')
flask.add_adjectives('small', 'clear', 'glass')
flask.set_max_volume_carried(0.050)
flask.set_max_weight_carried(200)
flask.liquid = True

flask.insert(water)
flask.insert(molasses)

potion_storage.insert(flask)

scroll = Scenery('scroll', 'scroll', 'This scroll appears to say something on it.')
scroll.add_adjectives('first')
scroll.unfix()
scroll.add_response(['read'], 'On the scroll there are theese words:\nMake a potion to hide thyself. Use this potion to sneak past an unbeatable enemy.\nDue next class.')
