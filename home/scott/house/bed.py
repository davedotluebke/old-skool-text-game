from container import Container
from thing import Thing
import gametools
import action

class Bed(Container):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, default_name, path, dreamland):
        super().__init__(default_name, path)
        self.closable = False
        self.fix_in_place('Moving the bed would require a lot of effort.')
        self.set_prepositions('on', 'onto', 'atop')
        self.dreamland = dreamland
    
    #
    # OTHER EXTERNAL METHODS (misc externally visible methods)
    #
    def wake_up(self, cons):
        cons.user.perceive('You wake up.')
        self.emit('&nD%s wakes up.', cons.user.id)
        cons.user.move_to(self.location)

    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    # 
    def lay(self, p, cons, oDO, oIDO):
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if sV == 'sleep':
            cons.user.move_to(self)
            cons.user.perceive('You lie down on the bed and fall fast asleep.')
            self.emit('&nD%s lies down on the bed and falls asleep.' % cons.user.id)
            cons.user.move_to(gametools.load_room(self.dreamland))
            Thing.game.schedule_event(70, self.wake_up, cons)
            return True
        if sV == 'lay' and sIDO == 'bed':
            cons.user.move_to(self)
            cons.user.perceive('You lay down on the bed and relax.')
            return True
        return "Did you mean to lay down on the bed?"
    
    def stand(self, p, cons, oDO, oIDO):
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if sV == 'stand':
            cons.user.move_to(self.location)
            cons.user.perceive('You stand up.')
            self.emit('&nD%s stands up.', cons.user.id)
            return True
        return 'Did you intend to stand up?'

    actions = dict(Container.actions)
    actions['lay'] =   action.Action(lay, True, True)
    actions['sleep'] = action.Action(lay, True, True)
    actions['stand'] = action.Action(stand, True, True)

#
# MODULE-LEVEL FUNCTIONS (e.g., clone() or load())
#
def clone():
    bed = Bed('bed', __file__, 'domains.school.forest.forest3')
    bed.set_description('soft, comfortable bed', 'This bed is soft and comfortable. It has white sheets on it.')
    return bed
