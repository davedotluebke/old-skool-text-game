import thing
import action
import gametools

class PlaceChooser(Thing):
	def __init__(self, ID, path, fixed_to):
		super().__init__(ID, path)
		self.written_on = 'domains.school.forest.woods'
		self.actions.append(action.Action(self.write, ['write'], True, False))
		self.fix_in_place('This paper is fixed to the %s with sorcery.' % fixed_to)
		self.set_description('magical piece of paper', 'This magical paper says "woods" on it.')
		self.add_names('paper')
		self.add_adjectives('magical')

	def write(self, p, cons, oDO, oIDO):
		try:
			self.written_on = " ".join(p.words[1:])
		except IndexError:
			return 'Did you mean to write something on the paper?'
		del self.location.exits['west']
        if gametools.validate_func(self.written_on, 'load'):
            self.location.exits['west'] = self.written_on
            cons.write('You write %s on the paper and feel a magical shift occur.' % self.written_on)
            parts = self.written_on.split('.')
            self.emit('&nD%s writes %s on the paper.' % (cons.user, parts[-1]))
        else:
            cons.write('The text on the paper morphs back into the words "woods".')
            self.written_on = 'domains.school.forest.woods'
            self.location.exits['west'] = self.written_on
        parts = self.written_on.split('.')
		self.long_desc = 'This magical paper says "%s" on it.' % parts[-1]
		return True

def clone():
    magical_paper = PlaceChooser('magical paper', 'wall')
    return magical_paper
