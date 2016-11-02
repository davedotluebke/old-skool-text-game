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
        self.actions = []
        self.actions.append(Action(self.look_at, ["look", "examine"], True, True))
        self.actions.append(Action(self.take, ["take", "get"], True, False))
        self.actions.append(Action(self.drop, ["drop"], True, False))

    def add_names(self, *sNames):
        """Add one or more strings as possible noun names for this object, each as a separate argument"""
        self.names += list(sNames)

    def add_adjectives(self, *sAdjs):
        """Add one or more adjective strings, each as a separate argument"""
        self.adjectives += list(sAdjs)
    
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

    def move_to(self, dest):
        """Extract this object from its current location and insert into dest. 
        Returns True if the move succeds. If the insertion fails, attempts to 
        re-insert into the original location and returns False."""
        origin = self.location
        if origin:
            origin.extract(self)
        # if cannot insert into destination, return to where it came from
        if not dest.insert(self):  # dest.insert returns True if insertion fails
            return True
        else:
            if (origin):
                origin.insert(self)
            return False

    # TODO: plumb validation protocol down to move_to(), insert(), extract()
    def take(self, p, cons, oDO, oIDO, validate):
        msg = True
        if oDO != self:
            msg = "You can't take that!"
        elif self.fixed:
            msg = self.error_message 
        if validate:
            return msg
        if msg != True: 
            cons.write(msg)
            return 
        if self.move_to(cons.user):
            cons.write("You take the %s." % self.id)
        else:
            cons.write("You cannot take the %s." % self.id)

    def drop(self, p, cons, oDO, oIDO, validate):
        msg = True
        if oDO != self:
            msg = "You can't take that!"
        elif self.fixed:
            msg = self.error_message 
        if validate:
            return msg
        if msg != True: 
            cons.write(msg)
            return
        if self.move_to(cons.user.location):
            cons.write("You drop the %s." % self.id)
        else:
            cons.write("You cannot drop the %s" % self.id)

    def look_at(self, p, cons, oDO, oIDO, validate):  
        '''Print out the long description of the thing.'''
        dbg.debug("Called Thing.look_at()")
        if (validate): 
            if oDO == self:
                return True
            else: 
                return "Not sure what you are trying to look at!"
        cons.write(self.long_desc)

