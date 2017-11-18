from thing import Thing
from container import Container

class Couch(Container):
	def __init__(self, default_name, path):
		super().__init__(default_name, path)
		self.actions.append(Action(self.sit, ["sit"], True, True))
		self.actions.append(Action(self.stand, ['stand'], True, True))
		self.closable = False
		self.fix_in_place('Moving the couch would require a lot of effort.')
		self.set_prepositions('on', 'onto')

	def sit(self, p, cons, oDO, oIDO):
		if oIDO == self:
			cons.write('You sit on the couch.')
			self.emit('&nD%s sits on the couch.' % cons.user.id)
			return True
		return 'Not quite sure what you ment.'
	
	def stand(self, p, cons, oDO, oIDO):
		(sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
		if sV == 'stand':
			cons.user.move_to(self.location)
			cons.write('You stand up.')
			self.emit('&nD%s stands up.' % cons.user.id)
			return True
		return 'Did you intend to stand up?'

def clone():
    couch = Couch('couch', __file__)
    couch.set_description('nice leather couch', 'This is a nice leather couch. You want to sit on it.')
    return couch
