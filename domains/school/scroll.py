from thing import Thing
from action import Action
from room import Room

class Scroll(Thing):
    def __init__(self, default_name, path, pref_id=None):
        super().__init__(default_name, path, pref_id)
        self.set_description('scroll', 'This scroll appears to say something on it.')
        self.actions.append(Action(self.read, ['read'], True, False))
        self.messages = ['Make a potion to hide thee. Use this potion to sneak past an unbeatable enemy.\nDue next class.', 'Thou must continue on thy journey\nAnd in thy journey\nThou must choose a path\nAnd thou must be careful, because thy choice defines thy destiny. ', 'Now that thou hast found thy power, thou must set off into the world.\nExplore the lands of Sorcery and Wizardry, Enchantment and Witchcraft. A letter will arrive for thee awaiting thy return.\n\nWrite the true name of a place on the magic paper, and go west to travel there. Write "learn wizardry", and go west to learn wizardry; or write "learn witchcraft" to learn witchcraft, "learn sorcery" to learn sorcery or "learn enchantment" to learn enchantment.']
        self.message_number = 0
        self.triggers = ['domains.school.dungeon.dungeon_hall','domains.school.elementQuest.waterfall','EOFError no more Scroll messages;']
        self.next_trigger_room = 'scrollchangeroom1'
        self.glow_when_enter_rooms = [['domains.school.elementQuest.path_choice', False]]

    def heartbeat(self):
        if self.location.id == self.next_trigger_room:
            self.emit('The scroll glows for a second!')
            self.message_number += 1
            self.next_trigger_room = self.triggers[self.message_number]
        for i in self.glow_when_enter_rooms:
            if i[1] == self.location:
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