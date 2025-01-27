from thing import Thing
from action import Action
import gametools

class CommunicationScroll(Thing):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self):
        super().__init__('scroll', __file__)
        self.written_on = ''
        self.set_description('tattered scroll', 'This scroll is tattered, but you can still make out the following: ')
        self.add_adjectives('tattered')
        
        self.other_scroll_id = None

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
        del self.location.west_door.dest
        try:
            self.location.west_door.dest = self.written_on
            gametools.load_room(self.written_on)
        except KeyError:
            cons.write('The text on the paper morphs back into the word "water_kitchen".')
            self.written_on = 'domains.school.school.water_kitchen'
            self.location.west_door.dest = Thing.ID_dict[self.written_on]
        self._long_desc = 'This magical paper says "%s" on it.' % self.written_on
        return True

    actions = dict(Thing.actions)  # make a copy
    actions['write'] = Action(write, True, False)

#
# MODULE-LEVEL FUNCTIONS (e.g., clone() or load())
#
def clone():
    paper = PlaceChooser('paper', __file__)
    return paper