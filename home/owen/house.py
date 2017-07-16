import time

from debug import dbg

from gameserver import Game
from action import Action
from thing import Thing
from container import Container
from room import Room  
from creature import Creature 
from creature import NPC
from player import Player
from console import Console
from scenery import Scenery
from liquid import Liquid
from weapon import Weapon
from armor import Armor
from book import Book

from domains.school.bookcase import Bookcase
from domains.school.sink import Sink
from domains.school.flower import Flower

class Bed(Container):
	def __init__(self, default_name):
		super().__init__(default_name)
		self.actions.append(Action(self.lay, ["lay", "sleep"], True, True))
		self.actions.append(Action(self.stand, ['stand'], True, True))
		self.closable = False
		self.fix_in_place('Moving the bed would require a lot of effort.')
		self.set_prepositions('on', 'onto', 'atop')
	
	def lay(self, p, cons, oDO, oIDO):
		(sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
		if sV == 'sleep':
			cons.user.move_to(self)
			cons.write('You lie down on the bed and fall fast asleep.')
			time.sleep(1)
			cons.write('You wake up.')
			return True
		if sV == 'lay' and sIDO == 'bed':
			cons.user.move_to(self)
			cons.write('You lay down on the bed and relax.')
			return True
		return "Did you mean to lay down on the bed?"
	
	def stand(self, p, cons, oDO, oIDO):
		(sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
		if sV == 'stand':
			cons.user.move_to(self.location)
			cons.write('You stand up.')
			return True
		return 'Did you intend to stand up?'

class Couch(Container):
	def __init__(self, default_name):
		super().__init__(default_name)
		self.actions.append(Action(self.sit, ["sit"], True, True))
		self.actions.append(Action(self.stand, ['stand'], True, True))
		self.closable = False
		self.fix_in_place('Moving the couch would require a lot of effort.')
		self.set_prepositions('on', 'onto')

	def sit(self, p, cons, oDO, oIDO):
		if oIDO == self:
			cons.write('You sit on the couch.')
			return True
		return 'Not quite sure what you ment.'
	
	def stand(self, p, cons, oDO, oIDO):
		(sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
		if sV == 'stand':
			cons.user.move_to(self.location)
			cons.write('You stand up.')
			return True
		return 'Did you intend to stand up?'

class FaucetThing(Thing):
	def __init__(self, ID, short_desc, long_desc, TYPE):
		super().__init__(ID)
		self.type = TYPE
		self.set_description(short_desc, long_desc)
		self.fix_in_place("You can't take the %s!" % self.type)
		self.add_names('faucet')
		self.actions.append(Action(self.fill_container, ["fill"], True, False))
		self.actions.append(Action(self.pour_out_in_self, ['pour'], True, False))
		self.actions.append(Action(self.toggle, ['turn'], True, True))
		self.running = 0
	
	def _adjust_descriptions(self):
		if self.running == 1:
			self.short_desc += ', with the water running'
			self.long_desc += ' The water in the %s is running.' % self.type
		if self.running == 0:
			(head, sep, tail) = self.short_desc.partition(", with the water running")
			self.short_desc = head
			(head, sep, tail) = self.long_desc.partition(" The water in the %s is running." % self.type)
			self.long_desc = head
		
	def toggle(self, p, cons, oDO, oIDO):
		(sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
		if sV == "turn":
			# could be "turn water on", "turn off water", etc
			if oDO == self and sIDO is not None: 
				return "I'm not sure what you mean."
			if (oDO == None and (oIDO == self or sDO == 'water')) or (oDO == self or sIDO == 'water'):
				if sPrep == "on":
					if self.running == 0:
						self.running = 1
						cons.write("You turn on the water.")
					else: 
						cons.write("The water is already on!")
				elif sPrep == "off":
					if self.running == 0:
						cons.write("The water is already off!")
					else:
						self.running = 0
						cons.write("You turn off the water.")
				else: # sPrep is some other preposition
					return "I'm not sure what you mean."
				self._adjust_descriptions()
				return True
		return "I don't know what you mean by %s in this context." % sV
	
	def fill_container(self, p, cons, oDO, oIDO):
		if oDO == None: 
			return "What do you intend to fill from the %s?" % self.type
		
		filling = oDO
		if not getattr(filling, 'liquid'):
			cons.write('The water leaves the %s and goes down the drain in the %s.' % (filling, self.type))
			return True
		cons.write('Water comes out of the faucet and fills your %s.' % filling)
		self.emit('The %s is filled with water at the %s.' % (filling, self.type))
		water = Liquid('water', 'some normal water', 'This is some normal clear water.')
		water.add_response(['drink'], 'You take a big drink of the water, and your thirst is quenched.')
		oDO.insert(water)
		return True
	
	def pour_out_in_self(self, p, cons, oDO, oIDO):
		if oDO:
			obj = oDO
		else:
			obj = oIDO
		if obj == self or obj == None:
			return "Imposible to pour out a %s in a %s." % (self.type, self.type)
		cons.write('You pour the %s into the %s, and it goes down the drain.' % (obj, self.type))
		obj.move_to(Thing.ID_dict['nulspace'])
		return True

class PlaceChooser(Thing):
	def __init__(self, ID, fixed_to):
		super().__init__(ID)
		self.written_on = 'woods'
		self.actions.append(Action(self.write, ['write'], True, False))
		self.fix_in_place('This paper is fixed to the %s with sorcery.' % fixed_to)
		self.set_description('magical piece of paper', 'This magical paper says "woods" on it.')
		self.add_names('paper')
		self.add_adjectives('magical')

	def write(self, p, cons, oDO, oIDO):
		try:
			self.written_on = " ".join(p.words[1:])
		except IndexError:
			return 'Did you mean to write something on the paper?'
		cons.write('You write %s on the paper and feel a magical shift occur.' % self.written_on)
		del self.location.exits['west']
		try:
			self.location.exits['west'] = Thing.ID_dict[self.written_on]
		except KeyError:
			cons.write('The text on the paper morphs back into the words "woods".')
			self.written_on = 'woods'
			self.location.exits['west'] = Thing.ID_dict[self.written_on]
		self.long_desc = 'This magical paper says "%s" on it.' % self.written_on
		return True

living_room = Room('living room', pref_id='lr31795')
bathroom = Room('bathroom', pref_id='btr31795')
bedroom = Room('bedroom', pref_id='br31795')
magic_room = Room('magical room', pref_id='mr31795')

living_room.set_description('well-kept living room', 'This is a comfortable living room, while quite small. It has a couch on one wall.')
bathroom.set_description('modern bathroom', 'This small bathroom has a bathtub, a shower, and a sink.')
bedroom.set_description('normal bedroom', 'This bedroom is small but nice. There are bookshelves on the walls and a great big window overlooking Firlefile sorcery school. ')
magic_room.set_description('magical room', 'This room has a lot of magical supplies. It also has a door on the west side of the room with a piece of paper above it.')

living_room.add_exit('west', bathroom.id)
living_room.add_exit('up', bedroom.id)
living_room.add_exit('south', magic_room.id)
bathroom.add_exit('east', living_room.id)
bedroom.add_exit('down', living_room.id)
magic_room.add_exit('north', living_room.id)
magic_room.add_exit('west', 'woods')

living_room.add_names('room', 'space')
living_room.add_adjectives('living', 'well-kept', 'comfortable')
bathroom.add_adjectives('modern')
bedroom.add_adjectives('small', 'comfortable')
magic_room.add_names('room')
magic_room.add_adjectives('magic', 'magical')

#in magical room

magical_paper = PlaceChooser('magical paper', 'wall')
magical_paper.move_to(magic_room)

# in bedroom
bed = Bed('bed')
bed.set_description('soft, comfortable bed', 'This bed is soft and comfortable. It has white sheets on it.')
bed.move_to(bedroom)
# in bathroom
bathtub = FaucetThing('bathtub', 'white bathtub', 'This bathtub is white. It has a faucet on one end of the tub and a shower above.', 'bathtub')
bathtub.add_adjectives('modern', 'white')
bathtub.move_to(bathroom)

sink = FaucetThing('sink', 'porcelin sink', 'This is a ordinary bathroom sink made of porcelin. It has a clean metal faucet.', 'sink')
sink.add_adjectives('porcelin', 'metal', 'clean', 'modern')
sink.move_to(bathroom)

toilet = Scenery('toilet', 'ordinary toilet', 'This is an ordinary toilet.')
toilet.add_response(['flush'], 'You flush the toilet.')
toilet.move_to(bathroom)

cabnet = Container('cabnet')
cabnet.set_description('small cabnet', 'This is a small cabnet above the sink.')
cabnet.add_adjectives('small')
cabnet.close()
cabnet.closable = True
cabnet.set_max_volume_carried(20)
cabnet.set_max_weight_carried(1000000)
cabnet.move_to(bathroom)
# in living room

bookshelf = Container('bookshelf')
bookshelf.set_description('oak bookshelf', 'This bookshelf is made of oak. It has many different books on it.')
bookshelf.closable = False
bookshelf.add_adjectives('oak')
bookshelf.add_names('shelf')
bookshelf.move_to(living_room)

couch = Couch('couch')
couch.set_description('nice leather couch', 'This is a nice leather couch. You want to sit on it.')
couch.move_to(living_room)

blue_book = Book("blue book", "newer light blue book", "This book is newer, sky blue, and says \"Dragonsky\" on the cover.")
blue_book.add_names("book", "Dragonsky")
blue_book.add_adjectives("blue", "newer", "light")
blue_book.set_message('''

Dragonsky

by Owen Luebke
#*
Chapter 1
	Once upon a time there were two twins. One was named Skylar and the other was named Jennifer. They were each other’s best friends too. They both enjoyed writing. Skylar wrote mostly poetry, and Jennifer wrote some non-fiction and a lot of autobiography, which was in a long book she wrote about her and Skylar’s lives. Her book stretched back to when she first learned to write at age 3, quite early. Their local elementary school was very supportive of their writing, and they were happy there. 
	Skylar and Jennifer happened to live in Kenshalk, and it was a great fit for them. Jennifer wrote a lot about the historic buildings, and they both enjoyed the brightly colored streetcars. They even lived in one of the houses overlooking the expansive KTA museum and the tracks beyond. 
	Skylar and Jennifer had many adventures. Occasionally they went camping, or they would visit places in town. They even went to other cities sometimes. They liked adventures almost anywhere. 
	They had a treehouse up in one of the trees near the fence. They were not afraid of heights at all. In fact, they enjoyed feeling like they were flying from a high height. Sometimes sat up in the treehouse and wrote things. Skylar wrote many poems there, such as:
		The wind rustles the leaves
		In the spring
		And it seems like fall

		The sun glares down
		In the spring
		And it seems like summer

		The bare trees sit
		In the spring
		And it seems like winter

		Then the trees bloom
		In the spring
		And it seems like spring
	They were preparing for their 12th birthday party. They were born in May, and so it happened as the school year let out. It was at
#*
Bounce Away!® because they liked to feel like they were flying, and the trampoline park did a pretty good job. Their entire class was invited, as well as some 4th graders and siblings of friends. It was a big group, and miraculously everyone could come. It was a really exciting event for everyone.
	The day of the party was dreary and wet, but warm, so Skylar and Jennifer were happy they chose an indoor activity. Waiting at stoplight after stoplight on route 95 only made them more and more excited. When they arrived, they met everybody else quickly, and went in. The party had started.
	They had a great time. They raced around, and they bounced in circles. And they tried to see who could jump the highest. Skylar and Jennifer were winning against everyone else. And they started jumping higher and higher. Then they both, at the same time, stuck out their arms and jumped even higher, and then started moving onto other trampolines. “Wee! We’re flying!” said Skylar. And then everyone started pretending to fly, and zipped around with their arms out. Skylar and Jennifer were bouncing so crazily that they had a hard time stopping before they went to their house for cake and ice cream.

	That night, as they lay in their beds, they talked about the day.
	“My favorite part was pretending to fly,” said Jennifer.
	“I agree. We jumped really high.” said Skylar.
	“We did. I was a good thing we didn’t hit the ceiling.”
	“It reminded me of when we first jumped on a trampoline when we were 3.”
	“Yeah. It was almost like we were actually flying.”
	Skylar did not respond right away. His mind went to the trampoline at age 3, to an experience where he fell down a few stairs, and to today. When he replied, it was in a whisper. He said:
	“I think maybe we can fly.”
	“Maybe,” Jennifer whispered back, after a short pause.
	“After another short pause, Skylar said, “I’m going to try.”
	He got out of bed, and stood in the middle of the room. He just stood there for a second, then he moved his arms up and down. Slowly but surely, he rose off the ground. Jennifer just stared.
	Then Jennifer got out of bed, and moved her arms up and down. She, too, went slowly but surely up into the air. They both looked at each other. 
	“Come on, let’s fly to the tree house!” said Skylar. He and Jennifer shoved open the old window, trying to keep it from squeaking or slamming shut on them. Eventually, they forced it open, and wedged it open. They both stepped out onto the windowsill. 
#*
	The warm rain drizzled down on them. It was not very strong anymore, just a little harder than mist. The ground was moist, visible from the second story window. It drizzled on.
	Skylar and Jennifer both stood for a second on the windowsill, gazing out upon the woods, before they took off into the rainy night. Flying down to the treehouse, they twisted and turned and fell in crazy somersaults. They rocketed up and down, right and left, and broke a few small branches. They tried to aim for the treehouse, but it was no good. They went up above the treehouse. Skylar came to a stop. He stood there for a second and looked out.
	Unfortunately, Jennifer’s landing was unexpected. She was a foot over the treehouse roof when she just dropped. “Ow!” she said quietly
	“I’ve got one thing I want you to agree to,” said Skylar in a hushed voice.
	“Is it ‘Don’t tell anyone’?” Jennifer whispered back.
	“Yes!” replied Skylar.
	They looked out over the KTA train museum and Banké Pacific tracks. No trains were running at the KTA museum, and one battered boxcar was sitting in the shadows on the Banké Pacific tracks. It said, “Banké Pacific Freight Express” and looked forlorn by itself.
	An occasional car zipped past about once a minute on the road. The bright lights and sound of the wheels on the asphalt, as well as the new pavement and bright lines, made the road seem more active and important than the tracks and museum. The streetlights shone down brightly.
	The warm rain trickled down, and the sound of dripping filled the air. It was light, but it was in a pattern almost, dripping as if it was part of a song. It was a nice sound, and dripped melodically.
	Finally, Skylar and Jennifer departed back to their house. They went shooting up in the air as soon as they took off, and then tore straight for their windowsill. Skylar had to kick off the brick to stop himself. Then they slid into their room, jiggled their window down, trying to keep it from slamming or squeaking, and jumped back into their beds, where they lay wondering what they had discovered.
#*
''')
blue_book.move_to(bookshelf)
