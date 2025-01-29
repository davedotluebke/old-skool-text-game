from thing import Thing
from action import Action
import gametools

import random
import os

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
        
        self.text_storage = 'communication_scroll_text.txt'
        
        self.game.register_heartbeat(self)
        
        self.log.debug('Finished the __init__ function of communication_scroll!')

    #
    # GET/SET METHODS
    #
    def heartbeat(self):
        try:
            with open(os.path.dirname(__file__) + '/' + self.text_storage) as f:
                new_text = f.read()
                if new_text != self.written_on:
                    self.emit('The ink on the scroll suddenly shifts, forming new words!')
                    self.written_on = new_text
        except FileNotFoundError:
            self.log.error("Couldn't find file at " + os.path.dirname(__file__) + '/' + self.text_storage)

    def update_other_scrolls(self):
        with open(os.path.dirname(__file__) + '/' + self.text_storage, 'w') as f:
            f.write(self.written_on)

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
        self.update_other_scrolls()
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
