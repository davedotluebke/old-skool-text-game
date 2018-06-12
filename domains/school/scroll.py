from thing import Thing
from action import Action
from room import Room

class Scroll(Thing):
    def __init__(self, default_name, path, pref_id=None):
        super().__init__(default_name, path, pref_id)
        self.set_description('scroll', 'This scroll appears to say something on it.')
        self.actions.append(Action(self.read, ['read'], True, False))
        self.messages = ['Make a potion to hide thee. Use this potion to sneak past an unbeatable enemy.\nDue next class.', 
        'Thou must continue on thy journey\nAnd in thy journey\nThou must choose a path\nAnd thou must be careful, because thy choice defines thy destiny. ',
        'Thy class begins shortly.']
        self.message_number = 0
        self.triggers = ['domains.school.dungeon.dungeon_hall', 'domains.school.school.great_hall']
        self.next_trigger_room = self.triggers[0]
        self.glow_when_enter_rooms = [['domains.school.elementQuest.path_choice', False]]
        Thing.game.register_heartbeat(self)

    def heartbeat(self):
        r = self
        while r.location:
            r = r.location
        
        if r.id == self.next_trigger_room:
            self.emit('The scroll glows for a second!')
            self.message_number += 1
            self.next_trigger_room = self.triggers[self.message_number]
        for i in self.glow_when_enter_rooms:
            if i[1] == r.id:
                self.emit('The scroll glows for a second!')
                i[2] == True

    def read(self, p, cons, oDO, oIDO):
        if oDO != self:
            return "Are you intending to read the scroll?"
        if len(p.words) == 2:
            cons.write('On the scroll there are these words:\n'+self.messages[self.message_number])
            return True
        else:
            return "A problem occurred!"

def clone(): 
    obj = Scroll('scroll', __file__)
    return obj