from container import Container
from thing import Thing
import gametools
import action

class Bed(Container):
    def __init__(self, default_name, path, dreamland):
        super().__init__(default_name, path)
        self.actions.append(action.Action(self.lay, ["lay", "sleep"], True, True))
        self.actions.append(action.Action(self.stand, ['stand'], True, True))
        self.closable = False
        self.fix_in_place('Moving the bed would require a lot of effort.')
        self.set_prepositions('on', 'onto', 'atop')
        self.dreamland = dreamland
    
    def lay(self, p, cons, oDO, oIDO):
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if sV == 'sleep':
            cons.user.move_to(self)
            cons.write('You lie down on the bed and fall fast asleep.')
            self.emit('&nD%s lies down on the bed and falls asleep.' % cons.user.id)
            cons.user.move_to(gametools.load_room(self.dreamland))
            Thing.game.events.schedule(30, self.wake_up, cons)
            return True
        if sV == 'lay' and sIDO == 'bed':
            cons.user.move_to(self)
            cons.write('You lay down on the bed and relax.')
            return True
        return "Did you mean to lay down on the bed?"
    
    def wake_up(self, cons):
        cons.write('You wake up.')
        self.emit('&nD%s wakes up.', cons.user.id)
        cons.user.move_to(self.location)

    def stand(self, p, cons, oDO, oIDO):
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if sV == 'stand':
            cons.user.move_to(self.location)
            cons.write('You stand up.')
            self.emit('&nD%s stands up.', cons.user.id)
            return True
        return 'Did you intend to stand up?'

def clone():
    bed = Bed('bed', __file__, 'domains.school.school.forest3')
    bed.set_description('soft, comfortable bed', 'This bed is soft and comfortable. It has white sheets on it.')
    return bed
