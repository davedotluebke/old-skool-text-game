from thing import Thing
from action import Action
from room import Room

class Scroll(Thing):
    def __init__(self, default_name, pref_id=None):
        super().__init__(default_name, pref_id)
        self.set_description('scroll', 'This scroll appears to say somthing on it.')
        self.actions.append(Action(self.read, ['read'], True, False))
        self.messages = ['Make a potion to hide thyself. Use this potion to sneak past an unbeatable enemy.\nDue next class.', 'Find thyself a power inside\nTake thee a large stride\nBe the one who does not cower\nAnd be the one who discovers the power\n\nFinish your task to find the power\nHere upon ticks your hour...\n\n']
        self.message_number = 0
        self.triggers = ['scrollchangeroom1','EOFError no more Scroll messages;']
        self.next_trigger_room = 'scrollchangeroom1'

    def heartbeat(self):
        if self.location:
            for l in range(1, 15):
                counter = eval('self.'+str(l*'location.'+'id'))
                if counter == self.next_trigger_room:
                    self.emit('The scroll glows for a second!')
                    self.message_number += 1
                    self.next_trigger_room = self.triggers[self.message_number]
                    break
                if isinstance(eval('self.'+str((l-1)*'location.')+'location'), Room) and counter != self.next_trigger_room:
                    break

    def read(self, p, cons, oDO, oIDO):
        if oDO != self:
            return "Are you intending to read the scroll?"
        if len(p.words) == 2:
            cons.write('On the scroll there are theese words:\n'+self.messages[self.message_number])
            return True
        else:
            return "A problem occured!"
