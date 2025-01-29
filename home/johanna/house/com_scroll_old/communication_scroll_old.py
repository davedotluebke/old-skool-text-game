from thing import Thing
from action import Action
import gametools

import random

class CommunicationScroll(Thing):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, pref_id=None, other_scroll_id=None):
        self.log.debug('In the __init__ function of communication_scroll!')
        super().__init__('scroll', __file__, pref_id=pref_id)
        self.written_on = 'This scroll is magical. Try writing on it.'
        self.set_description('tattered scroll', 'This scroll is tattered, but you can still make out the following: ' + self.written_on)
        self.add_adjectives('tattered')
        
        self.other_scroll_id = other_scroll_id
        
        self.log.debug('Finished the __init__ function of communication_scroll!')

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
def clone(params=[]):
    if len(params) == 2:
        matching_scroll_id=params[0]
        matching_location_path=params[1]
    else:
        matching_scroll_id = None
        matching_location_path = None
    
    scroll_id_number = f'communication_scroll{random.randint(0,100)}'
    scroll = CommunicationScroll(pref_id=scroll_id_number)
    
    if matching_scroll_id:
        scroll.other_scroll_id = matching_scroll_id
        scroll.debug('communication_scroll added other_scroll_id!')
    
    elif matching_location_path:
        scroll.debug('Decided to follow location path!')
        matching_location = gametools.load_room(matching_location_path)
        scroll.debug('Loaded location!')
        for i in matching_location.contents:
            if isinstance(i, CommunicationScroll):
                scroll.other_scroll_id = i.id
                i.other_scroll_id = scroll.id
                scroll.debug('Found and updated matching scroll!')

    return scroll
