from thing import Thing
from action import Action
from room import Room
from container import Container
from debug import dbg

class Scroll(Thing):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, default_name, path, pref_id=None):
        super().__init__(default_name, path, pref_id)
        self.set_description('scroll', 'This scroll appears to say something on it. Try "reading" it.')
        self.current_message = ''
        self.messages = {
            'domains.school.school.great_hall':        ['Make a potion to hide thee. Find the ancient recipe in the library. Use it to sneak past an unbeatable enemy.\nDue next class.', False],
            'domains.school.elementQuest.path_choice': ['Thou must continue on thy journey\nAnd in thy journey\nThou must choose a path\nAnd thou must be careful, because thy choice defines thy destiny. ', False],
            'domains.school.school.fire_lounge':       ['Thy class begins shortly.', False],
            'domains.school.school.water_lounge':      ['Thy class begins shortly.', False],
            'domains.school.school.earth_lounge':      ['Thy class begins shortly.', False],
            'domains.school.school.air_lounge':        ['Thy class begins shortly.', False]
        }
        Thing.game.register_heartbeat(self)
        self.user = None

    def _change_objs_to_IDs(self):
        super()._change_objs_to_IDs()
        try:
            if self.user:
                self.user = self.user.id
        except Exception:
            dbg.debug('something went wrong in the scroll (again!)')
    
    def _restore_objs_from_IDs(self):
        super()._restore_objs_from_IDs()
        try:
            if self.user:
                self.user = Thing.ID_dict[self.user]
        except Exception:
            dbg.debug('something went wrong in the scroll (again!)')

    def heartbeat(self):
        try:
            r = self.user.location
            if not isinstance(r, Room):
                return
        except AttributeError:
            dbg.debug('Error in scroll! No user with location')
            return
        if r.id in list(self.messages):
            if self.messages[r.id][1] == True:
                return
            else:
                self.emit('The scroll glows for a second!')
                self.current_message = self.messages[r.id][0]
                self.messages[r.id][1] = True

    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    # 
    def read(self, p, cons, oDO, oIDO):
        if oDO != self:
            return "Are you intending to read the scroll?"
        if len(p.words) == 2:
            cons.write('On the scroll there are these words:\n'+self.current_message)
            return True
        else:
            return "A problem occurred!"

    actions = dict(Thing.actions)
    actions['read'] = Action(read, True, False)

#
# MODULE-LEVEL FUNCTIONS (e.g., clone() or load())
#
def clone(): 
    obj = Scroll('scroll', __file__)
    return obj