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
        self.emit("The %s says: %s" % (self.names[0], speech))
        
class NPC(Creature):
    def __init__(self, ID, g, aggressive=0):
        Creature.__init__(self, ID)
        self.aggressive = aggressive
        self.act_frequency = 3  # how many heartbeats between NPC actions
        self.act_soon = 0       # how many heartbeats till next action
        self.choices = ['move_around', 'talk']  # list of things NPC might do
        self.enimies = []
        if self.aggressive:     # aggressive: 0 = will never attack anyone, even if attacked by them. Will flee. 1 = only attacks enimies. 2 = attacks anyone. highly aggressive.
            self.choices.append('attack')
        # list of strings that the NPC might say
        self.scripts = []
        self.current_script = None
        self.current_script_idx = 0

        g.register_heartbeat(self)
    
    def add_script(self, s):
        self.scripts.append(s)

    def heartbeat(self):
        self.act_soon += 1
        dbg.debug('beat')
        if self.act_soon == self.act_frequency or self.enimies in self.location.contents:
            self.act_soon = 0
            if self.current_script:  # if currently reciting, continue
                self.talk()
            for i in self.location.contents: # if an enimy is in room, attack
                if i in self.enimies and self.aggressive:
                    attack()
                elif i in self.enimies and not self.aggressive:  #can't attack (e.g. bluebird)? Run away.
                    self.move_around()
            else:                    # otherwise pick a random action
                choice = random.choice(self.choices)
                try:
                    choice_fn = getattr(self, choice)
                    choice_fn()
                except AttributeError:
                    dbg.debug("Object "+self.id+" heartbeat tried to run non-existant action choice "+choice+"!")
            
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
 
        self.emit("The %s goes %s." % (self.names[0], exit))
        current_room.extract(self)
 
        new_room.insert(self)
        self.emit("The %s arrives." % self.names[0])
        dbg.debug("Moved to new room %s" % (new_room.names[0]))
        return

    def talk(self):
        if self.scripts:
            if self.current_script:
                lines = self.current_script.splitlines()
                index = self.current_script_idx
                self.say(lines[index])
                self.current_script_idx += 1
                if self.current_script_idx == len(lines):
                    self.current_script = None
                    self.current_script_idx = 0
            else:
                self.current_script = random.choice(self.scripts)
    def attack(self):
        """Attack any enimies, if possible, or if highley aggressive, attack anyone in the room"""
        attacking = None
        for i in self.enimies:
            if i in self.location.contents:
                attacking = i
                continue
        if self.aggressive == 2 and not attacking:
            attacking = random.choice(hasattr(self.location.contents, hitpoints))
            self.enimies.append(attacking)
        dbg.debug(attacking.id)
