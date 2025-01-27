from thing import Thing
from action import Action
import gametools

class CommunicationScroll(Thing):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self):
        super().__init__('scroll', __file__)
        self.written_on = 'This scroll is magical'
        self.set_description('tattered scroll', 'This scroll is tattered, but you can still make out the following: ' + self.written_on)
        self.add_adjectives('tattered')
        
        self.other_scroll_id = None
    
    #
    # GET/SET METHODS
    #
    def update_other_scroll(self):
        

    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    # 
    def write(self, p, cons, oDO, oIDO):
        try:
            self.written_on = " ".join(p.words[1:])
        except IndexError:
            return 'Did you mean to write something on the scroll?'
        
        cons.user.perceive(f'You write {self.written_on} on the scroll.')
        self.emit(f'&nD{cons.user.id} writes something on the scroll.')
        self._long_desc = 'This scroll is tattered, but you can still make out the following: ' + self.written_on
        return True

    actions = dict(Thing.actions)  # make a copy
    actions['write'] = Action(write, True, False)
    actions['read']  = Action(Thing.look_at, True, False)

#
# MODULE-LEVEL FUNCTIONS (e.g., clone() or load())
#
def clone():
    scroll = CommunicationScroll()
    return scroll
