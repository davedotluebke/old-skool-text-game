from thing import Thing
from action import Action
from room import Room

class Scroll(Thing):
    def __init__(self, default_name, path, pref_id=None):
        super().__init__(default_name, path, pref_id)
        self.set_description('scroll', 'This scroll appears to say something on it.')
        self.actions.append(Action(self.read, ['read'], True, False))
        self.current_message = ''
        self.messages = {
            'domains.school.school.great_hall':        ['Make a potion to hide thee. Use this potion to sneak past an unbeatable enemy.\nDue next class.', False],
            'domains.school.dungeon.dungeon_hall':     ['Thou must continue on thy journey\nAnd in thy journey\nThou must choose a path\nAnd thou must be careful, because thy choice defines thy destiny. ', False],
            'domains.school.elementQuest.path_choice': ['Thou must continue on thy journey\nAnd in thy journey\nThou must choose a path\nAnd thou must be careful, because thy choice defines thy destiny. ', False],
            'domains.school.school.fire_lounge':       ['Thy class begins shortly.', False],
            'domains.school.school.water_lounge':      ['Thy class begins shortly.', False],
            'domains.school.school.earth_lounge':      ['Thy class begins shortly.', False],
            'domains.school.school.air_lounge':        ['Thy class begins shortly.', False]
        }
        Thing.game.register_heartbeat(self)

    def heartbeat(self):
        r = self
        while r.location:
            r = r.location
        
        if r.id in list(self.messages):
            if self.messages[r.id][1] == True:
                return
            else:
                self.emit('The scroll glows for a second!')
                self.current_message = self.messages[r.id][0]
                self.messages[r.id][1] = True

    def read(self, p, cons, oDO, oIDO):
        if oDO != self:
            return "Are you intending to read the scroll?"
        if len(p.words) == 2:
            cons.write('On the scroll there are these words:\n'+self.current_message)
            return True
        else:
            return "A problem occurred!"

def clone(): 
    obj = Scroll('scroll', __file__)
    return obj