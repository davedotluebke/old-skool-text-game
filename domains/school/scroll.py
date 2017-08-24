from thing import Thing
from action import Action
from room import Room

class Scroll(Thing):
    def __init__(self, default_name, path, pref_id=None):
        super().__init__(default_name, path, pref_id)
        self.set_description('scroll', 'This scroll appears to say somthing on it.')
        self.actions.append(Action(self.read, ['read'], True, False))
        self.messages = ['Make a potion to hide thyself. Use this potion to sneak past an unbeatable enemy.\nDue next class.', 'Thy must continue on thy journey\nAnd in thy journey\nThy must choose a path\nAnd thy must be careful, because thy choice defines thy destiny. ', 'Now that you have found your power, you must set off into the world.\nExplore the lands of Sorcery and Wizardry, Enchantment and Witchcraft. A letter will arrive for you awaiting your return.\n\nWrite the true name of a place on the magic paper, and go west to go there. Write "learn wizardry" and go west learn wizardry, "learn witchcraft" to learn witchcraft, "learn sorcery" to learn sorcery, and "learn enchantment" to learn enchantment.']
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
            cons.write('On the scroll there are theese words:\n'+self.messages[self.message_number])
            return True
        else:
            return "A problem occured!"

def clone(): 
    obj = Scroll('scroll', __file__)
    return obj