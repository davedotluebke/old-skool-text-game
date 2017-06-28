from room import Room
from thing import Thing
from action import Action

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

waterfall = Room('waterfall')
waterfall.set_description('beutiful waterfall base', 'This is a beutiful waterfall base. From here you can stand and look at the rushing waterfall. This place makes you feel peaceful inside, and happy. You will always remember this place.')
waterfall.add_adjectives('waterfall', 'beutiful', 'special')
waterfall.add_names('place', 'base')
waterfall.add_exit('west', Thing.ID_dict['woods'])

paper = PlaceChooser('magic paper', 'trunk of a tree')
paper.move_to(waterfall)
