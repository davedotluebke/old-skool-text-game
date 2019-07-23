import gametools
import room
import scenery
import action
from debug import dbg

class Waterfall(scenery.Scenery):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self):
        super().__init__('waterfall', 'rushing waterfall', 'This is a wide, rushing waterfall. '
        'It flows from above a rocky cliff to a large pool below.')
        self.add_adjectives('rushing')
    
    #
    # ACTION METHODS (dictionary must be built per-object for Scenery)
    # 
    def enter(self, p, cons, oDO, oIDO):
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if sDO == 'waterfall':
            if cons.user.wizardry_element != 'water':
                cons.user.perceive('You try to enter the waterfall, but get swept back by the rushing current.')
                cons.user.emit('&nD%s dives into the waterfall, but gets swept back by the rushing current.')
                return True
            dest = gametools.load_room('domains.school.school.water_lounge')
            if dest == None:
                cons.user.perceive("You try to enter the waterfall, but an error occurs! Please report it.")
                dbg.debug('Error! dest() of waterfall returned None on load!')
                return True
            cons.user.perceive('You dive into the waterfall, and find yourself somewhere quite different.')
            cons.user.emit('&nD%s dives into the waterfall and dissapears from view.')
            cons.user.move_to(dest)
            dest.report_arrival(cons.user)
            return True
        return "Did you mean to enter the waterfall?"
        

#
# MODULE-LEVEL FUNCTIONS (e.g., clone() or load())
#
def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = room.Room('base', roomPath)
    r.set_description('waterfall base', 'You look up to find yourself beside a waterfall base. '
    'To the north a rushing waterfall flows over a rocky ledge and plumets into the pool below. '
    'To the south a small stream trickles away.')
    r.add_adjectives('waterfall')
    r.add_exit('northwest', 'domains.school.forest.field')

    w = Waterfall()
    w.actions = dict(scenery.Scenery.actions)
    w.actions['enter'] = action.Action(w.enter, True, False)

    r.insert(w, True)

    return r
