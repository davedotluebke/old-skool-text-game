from debug import dbg
from action import Action
import random
import re

class Thing:
    ID_dict = {}

    def _add_ID(self, preferred_id):
        """Add object to Thing.ID_dict (the dictionary mapping IDs to objects).

        Takes a preferred ID string and (if necessary) creates a unique ID
        string from it. Returns the unique ID string. """
        self.id = preferred_id
        while self.id in Thing.ID_dict:     # unique-ify self.id if necessary
            self.id = self.id + str(random.randint(0, 9))
        Thing.ID_dict[self.id] = self
        return self.id

    def __init__(self, default_name):
        self.names = [default_name]
        self._add_ID(default_name)
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
        self.actions = [Action(self.look_at, ["look", "examine"], True, True), 
                        Action(self.take, ["take", "get"], True, False),
                        Action(self.drop, ["drop"], True, False)]

    def __str__(self): 
        return self.names[0]

    
    def clone_code(self, prefix):
        """Return code to duplicate this object (non-recursive). 

        Creates a string of Python code which, if executed, will re-create 
        this object. This is used instead of pickling when saving and 
        restoring player inventories, because objects a restored player
        is carrying should be added to the game as new objects rather than
        restoring references to existing objects. 
        
        Attributes consisting of standard Python types (int, string, list...)
        are saved directly. Attributes such as location and contents[], which
        consist of references to Thing objects (or subclasses thereof) store
        the object ID string from Thing.ID_dict instead, prepended with 
        <prefix> which should be a unique string. This ensures that when the
        code is executed it creates a new set of objects rather than finding 
        existing instances in the game with the same, original ID. 

        Note: this function does not recursively call clone_code() for such 
        referenced objects (contents of containers, etc).

        Note that subclasses of Thing may need to define their own
        clone_code() with additonal class-specific initialization code. """
        obj_class = self.__class__
        obj_module_name = str(obj_class.__module__)
        obj_class_name = re.search(r"<class (\S+)\.(\S+)'>", str(obj_class)).group(2)
        # build a string with code to import module and create an instance
        s = "from {mod} import {cls}; ".format(mod=obj_module_name, cls=obj_class_name)
        s += "_tmp = {cls}('{name}'); ".format(cls=obj_class_name, name=self.names[0])
        # add code to set attributes in new object to match attributes of self
        for k,v in sorted(self.__dict__.items()):
            # special-case actions, contents, and attached console
            if k in ('actions', 'cons', 'contents'):
                continue
            if isinstance(v, Thing): 
                v = prefix + v.id
            s += "_tmp.%s = %s; " % (k, repr(v))
        # deal with contents
        s += "_tmp.contents = " 
        s += ("[" + ", ".join(["'%s%s'" % (prefix, x.id) for x in self.contents]) + "]; ") if self.contents else "None; "
        # deal with actions 
        s += "_tmp.actions = []; \n"
        for a in self.actions:
            if a in self.__class__.actions: 
                continue
            s += "_tmp.actions.append(Action(%s, %s, %s, %s, %s)); \n" % \
            (a.func, a.verblist, a.transitive, a.intransitive, a.restrictions)
        return s


    def __getstate__(self): 
        """Custom pickling code for Thing.
        
        Doesn't pickle Thing.ID_dict (which refers to all objects in game).
        We will re-create this dictionary from scratch as we unpickle objects.
        To facilitate this, replace all references to other objects with 
        their unique ID strings. After unpickling we will replace these with
        the actual references. 
        """
        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()
        if self.location != None: 
            state['location'] = self.location.id
        #if self.contents != None: 
            # replace with new list of id strings, or leave as None (not [])
        #    state['contents'] = [x.id for x in self.contents] 
        return state

    def __setstate__(self, state):
        """Custom unpickling code for Thing.

        Re-create the Thing.ID_dict{} dictionary during unpickling:
        if an object's ID is in the dictionary (because some other object
        referred to it, e.g. via the location[] or contents[] fields)
        just leave it there; otherwise create its entry.

        After unpickling, another pass will be required to replace ID strings
        (in location and contents fields) with the actual object references.
        All objects end up in Thing.ID_dict, so we can just iterate over it.
        """
        # Restore instance attributes
        try: 
            obj = Thing.ID_dict[state['id']] # is this obj already in dict?
            dbg.debug("Note: %s already in Thing.ID_dict, maps to %s" % (state['id'], obj))
        except KeyError:  # 
            Thing.ID_dict[state['id']] = self
        self.__dict__.update(state)

    def _restore_objs_from_IDs(self):
        """Update object references stored as ID strings to directly reference the objects, using Thing.ID_dict."""
        if isinstance(self.location, str):
            self.location = Thing.ID_dict[self.location]
        if self.contents != None:
            self.contents = [Thing.ID_dict[id] for id in self.contents if isinstance(id, str)]
    
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
        if hasattr(self, 'invisible') and self.invisible == True:
            return
        # pass message to containing object, if it can receive messages
        holder = self.location
        if not holder: 
            #  this Thing is a room, pass message to all creatures in the room
            holder = self
        if holder not in ignore and hasattr(holder, 'perceive'):
            # immediate container can see messages, probably a creature/player
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
            cons.write("You take the %s." % self)
        else:
            cons.write("You cannot take the %s." % self)
        return True

    def drop(self, p, cons, oDO, oIDO):
        if oDO != self:     return "You can't drop that!"
        if self.fixed:      return self.fixed
        if self.location != cons.user: return "You aren't holding the %s!" % self.short_desc
        if self.move_to(cons.user.location):
            cons.write("You drop the %s." % self)
        else:
            cons.write("You cannot drop the %s" % self)
        return True

    def look_at(self, p, cons, oDO, oIDO):  
        '''Print out the long description of the thing.'''
        dbg.debug("Called Thing.look_at()")
        if self == oDO or self == oIDO:
            cons.write(self.long_desc)
            return True
        else:
            return "Not sure what you are trying to look at!"
        
