import random
from debug import dbg
from container import Container

class Creature(Container):
    def __init__(self, ID):
        Container.__init__(self, ID)
        self.hitpoints = 10           # default hitpoints
        self.health = self.hitpoints  # default full health (0 health --> dead)

    def perceive(self, message):
        """Receive a message emitted by an object carried by or in vicinity of this creature."""
        dbg.debug("perceived a message "+message+" in Creature.perceive()")

    def say(self, speech):
        """Emit a message to the room "The <creature> says: <speech>". """
        self.emit("The %s says: %s" % (self.id, speech))
        
class NPC(Creature):
    def __init__(self, ID, g):
        Creature.__init__(self, ID)
        self.aggressive = False
        self.act_frequency = 3  # how many heartbeats between NPC actions
        self.act_soon = 0       # how many heartbeats till next action
        self.actions = ['move_around', 'talk']  # list of action functions
        self.quotes = []        # list of strings that the NPC might say

        g.register_heartbeat(self)
    
    def add_quote(self, q):
        self.quotes.append(q)

    def heartbeat(self):
        self.act_soon += 1
        dbg.debug('beat')
        if self.act_soon == self.act_frequency:
            self.act_soon = 0
            action = random.choice(self.actions)
            try:
                action_fn = getattr(self, action)
                action_fn()
            except AttributeError:
                dbg.debug("Object "+self.id+" heartbeat tried to run non-existant action "+action+"!")
            
    def move_around(self):
        """The NPC leaves the room, taking a random exit"""
        try:
            exit_list = list(self.location.exits)
            exit = random.choice(exit_list)
        except (AttributeError, IndexError):
            dbg.debug('no exits, returning')
            return

        dbg.debug("Trying to move to the %s exit!" % (exit))
        current_room = self.location
        new_room = self.location.exits[exit]
 
        self.emit("The %s goes %s." % (self.id, exit))
        current_room.extract(self)
 
        new_room.insert(self)
        self.emit("The %s arrives." % self.id)
        dbg.debug("Moved to new room %s" % (new_room.id))
        return

    def talk(self):
        if self.quotes: 
            speech = random.choice(self.quotes)
            self.say(speech)
