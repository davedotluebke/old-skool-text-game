from thing import Thing
from action import Action
import gametools

import random

class CommunicationScroll(Thing):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, pref_id=None, other_scroll_id=None):
        super().__init__('scroll', __file__, pref_id=pref_id)
        self.written_on = 'This scroll is magical. Try writing on it.'
        self.set_description('tattered scroll', 'This scroll is tattered, but you can still make out the following: ' + self.written_on)
        self.add_adjectives('tattered')
        
        self.other_scroll_id = other_scroll_id
    
    #
    # GET/SET METHODS
    #
    def update_other_scroll(self):
        try:
	        other_scroll = Thing.ID_dict[self.other_scroll_id]
        except KeyError:
            self.log.debug("Error! Couldn't find matching scroll.")
         	return
        
        other_scroll.written_on = self.written_on
        other_scroll._long_desc = 'This scroll is tattered, but you can still make out the following: ' + self.written_on
        other_scroll.emit('The ink on the scroll suddenly shifts, forming new words!')

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
        self.update_other_scroll()
        return True

    actions = dict(Thing.actions)  # make a copy
    actions['write'] = Action(write, True, False)
    actions['read']  = Action(Thing.look_at, True, False)

#
# MODULE-LEVEL FUNCTIONS (e.g., clone() or load())
#
def clone(match_location=None):
    scroll_id_number = f'communication_scroll{random.randint(0,100)}'
    scroll = CommunicationScroll(pref_id=scroll_id_number)
    
    if match_location:
        other_scroll_id_number = f'communication_scroll{random.randint(0,100)}'
        other_scroll = CommunicationScroll(pref_id=other_scroll_id_number, other_scroll_id=scroll.id)
        scroll.other_scroll_id = other_scroll.id
        
        
    return scroll
