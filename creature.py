import random
from debug import dbg
from thing import Thing
from container import Container

class Creature(Container):
    def __init__(self, default_name):
        Container.__init__(self, default_name)
        self.closed = True
        self.see_inside = False
        self.hitpoints = 10           # default hitpoints
        self.health = self.hitpoints  # default full health (0 health --> dead)
        self.viewed = False
        self.armor_class = 0
        self.combat_skill = 0
        self.strength = 0
        self.dexterity = 0
        self.armor_worn = None
        self.wepon_weilding = None

    def set_combat_vars(self, armor_class, combat_skill, strength, dexterity):
        self.armor_class = armor_class
        self.combat_skill = combat_skill
        self.strength = strength
        self.dexterity = dexterity

    def look_at(self, p, cons, oDO, oIDO):
        '''Print out the long description of the creature.'''
        self.viewed = cons.user
        dbg.debug("Called Creature.look_at()")
        if self == oDO or self == oIDO:
            cons.write(self.long_desc)
            return True
        else:
            return "Not sure what you are trying to look at!"

    def perceive(self, message):
        """Receive a message emitted by an object carried by or in vicinity of this creature."""
        dbg.debug("perceived a message "+message+" in Creature.perceive()")

    def say(self, speech):
        """Emit a message to the room "The <creature> says: <speech>". """
        self.emit("The %s says: %s" % (self, speech))
        
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
                    attack(i)
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
 
        self.emit("The %s goes %s." % (self, exit))
        current_room.extract(self)
 
        new_room.insert(self)
        self.emit("The %s arrives." % self)
        dbg.debug("Moved to new room %s" % (new_room))
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
    def attack(self, enimy=None):
        """Attack any enimies, if possible, or if highley aggressive, attack anyone in the room"""
        attacking = enimy
        for i in self.enimies:
            if i in self.location.contents and not attacking:
                attacking = i
                continue
        if self.aggressive == 2 and not attacking:
            attacking = random.choice(hasattr(self.location.contents, hitpoints))
            self.enimies.append(attacking)
        dbg.debug(attacking.id)
        if not self.wepon_weilding:
            for w in self.contents:
                if hasattr(w, damage):
                    self.wepon_weilding = w
                    dbg.debug("wepon chosen: %s" % wepon_weilding)
                    continue
        if not self.armor_worn:
            for a in self.contents:
                if hasattr(a, damage_prevent_num):
                    self.armor_worn = a
                    dbg.debug("armor chosen: %s" % armor_worn)
                    continue
        chance_of_hitting_self = self.armor_class * self.armor_worn.damage_prevent_num
        chance_of_hitting_enimy = self.combat_skill * self.wepon_weilding.accuracy
        damage_done_self = self.wepon_weilding.damage - 1/self.strength
        attack_freq_self = self.dexterity * (1/self.wepon_weilding.unweildiness) * (1/self.armor_worn.unweildiness)

