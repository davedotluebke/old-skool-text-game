from debug import dbg
from action import Action
import random

class Thing:
    ID_dict = {}

    def __init__(self, default_name):
        self.names = [default_name]
        self.id = default_name
        while self.id in Thing.ID_dict:     # unique-ify self.id if necessary
            self.id = self.id + str(random.randint(0, 9))
        Thing.ID_dict[self.id] = self

        self.plural = False         # should this thing be treated as plural?
        self.weight = 0.0
        self.volume = 0.0
        self.emits_light = False
        self.location = None
        self.fixed = False          # False if unfixed, error message if fixed 
        self.short_desc = 'need_short_desc'
        self.long_desc = 'need_long_desc'
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
        self.fixed = error_message

    def unfix(self):
        self.fixed = False

    def set_description(self, s_desc, l_desc):
        self.short_desc = s_desc
        self.long_desc = l_desc

    def new_verb(self, verb, func):
        self.verb_dict[verb] = func
    
#    def conjugate(self, verb_infinitive, cons):
#        for i in self.conjugations:
#            if hasattr(i, 'cons'):
#                pass

    def heartbeat(self):
        pass

    def emit(self, message, ignore = []):
        """Write a message to be seen by creatures holding this Thing or in the same room, skipping creatures in the list <ignore>"""
        # pass message to containing object, if it can receive messages
        holder = self.location
        if not holder: 
            return 
        if holder not in ignore and hasattr(holder, 'perceive'):
            # immeidate container can see messages, probably a creature/player
            dbg.debug("creature holding this object is: " + holder.id)
            holder.perceive(message)
        # now get list of recipients (usually creatures) contained by holder (usually a Room)
        recipients = [x for x in holder.contents if hasattr(x, 'perceive') and (x is not self) and (x not in ignore)]
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
    def take(self, p, cons, oDO, oIDO):
        if oDO == None: return "I don't know what you're trying to take!"
        if oDO != self: return "You can't take the %s!" % oDO.short_desc
        if self.fixed:  return self.fixed 
        if self.location == cons.user: return "You are already holding the %s!" % self.short_desc
        if self.move_to(cons.user):
            cons.write("You take the %s." % self.names[0])
        else:
            cons.write("You cannot take the %s." % self.names[0])
        return True

    def drop(self, p, cons, oDO, oIDO):
        if oDO != self:     return "You can't drop that!"
        if self.fixed:      return self.fixed
        if self.location != cons.user: return "You aren't holding the %s!" % self.short_desc
        if self.move_to(cons.user.location):
            cons.write("You drop the %s." % self.names[0])
        else:
            cons.write("You cannot drop the %s" % self.names[0])
        return True

    def look_at(self, p, cons, oDO, oIDO):  
        '''Print out the long description of the thing.'''
        dbg.debug("Called Thing.look_at()")
        if oDO != self: 
            return "Not sure what you are trying to look at!"
        cons.write(self.long_desc)
        return True

