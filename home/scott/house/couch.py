from thing import Thing
from container import Container
from action import Action

class Couch(Container):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, default_name, path):
        super().__init__(default_name, path)
        self.closable = False
        self.fix_in_place('Moving the couch would require a lot of effort.')
        self.set_prepositions('on', 'onto')

    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    # 
    def sit(self, p, cons, oDO, oIDO):
        if oIDO == self:
            cons.user.perceive('You sit on the couch.')
            self.emit('&nD%s sits on the couch.' % cons.user.id)
            return True
        return 'Not quite sure what you ment.'
    
    def stand(self, p, cons, oDO, oIDO):
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if sV == 'stand':
            cons.user.move_to(self.location)
            cons.user.perceive('You stand up.')
            self.emit('&nD%s stands up.' % cons.user.id)
            return True
        return 'Did you intend to stand up?'

    actions = dict(Container.actions)  # make a copy
    actions['sit'] =   Action(sit, True, True)
    actions['stand'] = Action(stand, True, True)

#
# MODULE-LEVEL FUNCTIONS (e.g., clone() or load())
#
def clone():
    couch = Couch('couch', __file__)
    couch.set_description('nice leather couch', 'This is a nice leather couch. You want to sit on it.')
    return couch
