from debug import dbg
from action import Action

class Thing:
    def __init__(self, ID):
        self.id = ID
        self.weight = 0.0
        self.volume = 0.0
        self.location = None
        self.fixed = False
        self.short_desc = 'need_short_desc'
        self.long_desc = 'need_long_desc'
        self.names = [ID]   
        self.adjectives = []
        self.contents = None        # None - only Containers can contain things
        # dictionary mapping verb strings to functions:
        self.verb_dict = {}
        self.add_verb("look", self.look_at)
        self.add_verb("examine", self.look_at)
        self.add_verb("take", self.take)
        self.add_verb("get", self.take)
        self.add_verb("drop", self.drop)
        self.actions = []
        self.actions.append(Action(self.look_at, ["look", "examine"], True, True))
        self.actions.append(Action(self.take, ["take", "get"], True, False))
        self.actions.append(Action(self.drop, ["drop"], True, False))

    def add_name(self, sName):
        """Add the string sName as a possible noun name for this object"""
        self.names.append(sName)

    def add_adjective(self, sAdj):
        self.adjectives.append(sAdj)

    def add_verb(self, sVerb, fVerb):
        """Add the given string sVerb and function fVerb to the object's verb_dict{}."""
        self.verb_dict[sVerb] = fVerb

    def set_weight(self, grams):
        if (grams < 0):
            dbg.debug("Error: weight cannot be negative")
            raise
        else:
            self.weight = grams

    def set_volume(self, liters):
        if (liters < 0):
            dbg.debug("Error: volume cannot be negative")
            raise
        else:
            self.volume = liters

    def set_location(self, containing_object):
        self.location = containing_object

    def fix_in_place(self, error_message):
        self.fixed = True
        self.error_message = error_message

    def unfix(self):
        self.fixed = False

    def set_description(self, s_desc, l_desc):
        self.short_desc = s_desc
        self.long_desc = l_desc

    def new_verb(self, verb, func):
        self.verb_dict[verb] = func

    def heartbeat(self):
        pass

    def emit(self, message):
        """Write a message to be seen by creatures holding this Thing or in the same room"""
        # pass message to containing object, if it can receive messages
        holder = self.location
        if not holder: 
            return 
        if hasattr(holder, 'perceive'):
            # immeidate container can see messages, probably a creature/player
            dbg.debug("creature holding this object is: " + holder.id)
            holder.perceive(message)
        # now get list of recipients (usually creatures) contained by holder (usually a Room)
        recipients = {x for x in holder.contents if hasattr(x, 'perceive') and (x is not self)}
        dbg.debug("other creatures in this room include: " + str(recipients))
        for recipient in recipients:
            recipient.perceive(message)

    def look_at(self, p, cons, oDO, oIDO):  # print out the long description of the thing
        dbg.debug("Called Thing.look_at()")
        cons.write(self.long_desc)

    def move_to(self, p, cons, oDO, oIDO):
        if self.fixed:
            cons.write(self.error_message)
        else:
            if self.location != None:
                self.location.extract(self)
            if oDO.insert(self):
                return True

    def take(self, p, cons, oDO, oIDO):
        if  (oDO == self) and not self.fixed:
            if not self.move_to(p, cons, cons.user, oIDO):
                cons.write("You take the %s." % self.id)
            else:
                cons.write("You cannot take the %s." % self.id)

    def drop(self, p, cons, oDO, oIDO):
        if (oDO == self) and not self.fixed:
            self.move_to(p, cons, cons.user.location, oIDO)
            cons.write("You drop the %s." % self.id)
