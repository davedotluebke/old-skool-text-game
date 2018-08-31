from debug import dbg
from action import Action
import random
import gametools

class Thing(object):
    ID_dict = {}
    game = None

    def _add_ID(self, preferred_id):
        """Add object to Thing.ID_dict (the dictionary mapping IDs to objects).

        Takes a preferred ID string and (if necessary) creates a unique ID
        string from it. Returns the unique ID string. """
        self.id = preferred_id
        while self.id in Thing.ID_dict:     # unique-ify self.id if necessary
            self.id = self.id + str(random.randint(0, 9))
        Thing.ID_dict[self.id] = self
        return self.id

    def __init__(self, default_name, path, pref_id=None):
        self.unlisted = False # should this thing be listed in room description  
        self.path = gametools.findGamePath(path) if path else None
        self.version_number = 1
        self.names = [default_name]
        self._add_ID(default_name if not pref_id else pref_id)
        self.plurality = 1
        self._weight = 0.0
        self._volume = 0.0
        self.emits_light = False
        self.flammable = 0
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
        self.spawn_location = None
        self.spawn_interval = None
        self.spawn_message = None

    def __del__(self):
        dbg.debug('Deleting object: %s: %s.' % (self.names[0], self.id), 0)
    
    def delete(self):
        if self.contents:
            for i in self.contents:
                i.delete()
        if self.location:
            self.location.extract(self)
        del Thing.ID_dict[self.id]

    def __str__(self): 
        return self.names[0]

    def get_saveable(self):
        """Return dictionary of everything needed to save/restore the object

        Return a "saveable" version of the object: a dictionary containing a
        list of attributes THAT DIFFER from the default attributes for this 
        object. This dictionary can be saved to a file and the object can be
        restored by creating a default object and overwriting any attributes 
        listed in the saveable. 

        This allows objects to persist across changes to the object code. 
        """
        saveable = {}
        state = self.__dict__.copy()
        del state["actions"]
        default_obj = gametools.clone(self.path)
        default_state = default_obj.__dict__
        for attr in list(state):
            if state[attr] != default_state[attr] or attr == 'path' or attr == 'version_number':
                saveable[attr] = state[attr]
        return saveable

    def update_obj(self, savable):
        """Return the updated object from the "savable" version created above. 
        Also call update_version() to make sure that all objects are up to date."""
        state = self.__dict__.copy()
        for attr in list(savable):
            state[attr] = savable[attr]

        self.update_version()

        self.__dict__.update(state)

    def update_version(self):
        """Updates the version of the object, and runs snipets of code to make 
        sure all objects will still function."""
        if not self.version_number:
            self.version_number = 1

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
        if self.location:
            if not isinstance(self.location, str): 
                # if it isn't already a string, convert it to one 
                state['location'] = self.location.id
        if self.contents != None: 
            # replace with new list of id strings, or leave as None (not [])
            state['contents'] = [(x if isinstance(x, str) else x.id) for x in self.contents]
        if self in Thing.game.heartbeat_users:
            state['has_beat'] = True
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
        except KeyError:  # Not already in dict
            Thing.ID_dict[state['id']] = self
        if 'has_beat' in state:
            Thing.game.register_heartbeat(self)
        self.__dict__.update(state)

    def _restore_objs_from_IDs(self):
        """Update object references stored as ID strings to directly reference the objects, using Thing.ID_dict."""
        if isinstance(self.location, str):
            self.location = Thing.ID_dict[self.location] # XXX will this work correctly for the room if it isn't loaded yet? 
        if self.contents != None:
            self.contents = [Thing.ID_dict[id] for id in self.contents if isinstance(id, str)]

    def _change_objs_to_IDs(self):
        """Replace object references with ID strings, in preparation for pickling."""
        if self.location:
            self.location = self.location.id
        if self.contents:
            self.contents = [obj.id for obj in self.contents]

    def add_names(self, *sNames):
        """Add one or more strings as possible noun names for this object, each as a separate argument"""
        self.names += list(sNames)

    def add_adjectives(self, *sAdjs):
        """Add one or more adjective strings, each as a separate argument"""
        self.adjectives += list(sAdjs)
    
    def set_weight(self, grams):
        if (grams < 0):
            dbg.debug("Error: weight cannot be negative", 0)
            raise
        else:
            self.weight = grams
    
    def get_weight(self):
        '''Return the weight of a single object times the number of objects present'''
        return self._weight * self.plurality

    def set_volume(self, liters):
        if (liters < 0):
            dbg.debug("Error: volume cannot be negative", 0)
            raise
        else:
            self.volume = liters
    
    def get_volume(self):
        '''Return the volume of a single object times the number of objects present'''
        return self._volume * self.plurality

    def set_location(self, containing_object):
        self.location = containing_object

    def fix_in_place(self, error_message):
        self.fixed = error_message

    def unfix(self):
        self.fixed = False

    def set_description(self, s_desc, l_desc, unlisted=False):
        self.short_desc = s_desc
        self.long_desc = l_desc
        self.unlisted = unlisted

    def indefinite(self):
        """Return the appropriate indefinite article ('a' or 'an') to use with
        the object, based on starting character of self.short_desc. Overload  
        for objects not starting with a vowel that should still use 'an'"""
        return "an" if self.short_desc[0] in 'aeiou' else "a"

    def get_short_desc(self, perceiver=None, definite=False, indefinite=False):
        '''Return the short description of this object, optionally prepended
        by an article. Prepends with 'the' if <definite> is True, or with 'a'
        or 'an' if indefinite is true. Only one of definite/indefinite should 
        be set to true. The <perceiver> is the Creature (usually a Player) 
        for whom the description is intended. This allows the function to be
        overloaded for objects whose description depends on who is observing 
        it. For example, Creatures (like NPCs and Players) may have proper 
        names that will be used instead of a short description once the 
        Creature is introduced. Plural objects are described as 
        "{two/three/four/several/many/a {small/large/huge} pile of} <plural_short_desc>"'''
        if definite: 
            article = "the "
        elif indefinite:
            article = self.indefinite() + " "
        else:
            article = ""
        if self.plurality > 1:
            if   self.plurality == 2:        quantity = "two "  # TODO: consider package 'num2words' instead
            elif self.plurality == 3:        quantity = "three "
            elif self.plurality == 4:        quantity = "four "  
            elif 5 <= self.plurality <= 8:   quantity = "several "
            elif 9 <= self.plurality <= 15:  quantity = "many "
            elif 16 <= self.plurality <= 25: quantity = article + "pile of "
            elif 26 <= self.plurality <= 50: quantity = article + "large pile of "
            elif 51 <= self.plurality < 100: quantity = article + "huge pile of "
            elif 100 <= self.plurality:      quantity = article + "vast pile of "
            return quantity + if hasattr(self, plural_short_desc) self.plural_short_desc else self.short_desc+"s"
        else: 
            return article + self.short_desc

    def possessive(self):
        """Return 'his', 'her', or 'its' as appropriate."""
        if hasattr(self, 'gender'):
            if self.gender == 'male': 
                return 'his'
            elif self.gender == 'female':
                return 'her'
        return 'its'  

    def pronoun(self):
        """Return 'he', 'she', or 'it' as appropriate."""
        if hasattr(self, 'gender'):
            if self.gender == 'male': 
                return 'he'
            elif self.gender == 'female':
                return 'she'
        return 'it'

#    def conjugate(self, verb_infinitive, cons):
#        for i in self.conjugations:
#            if hasattr(i, 'cons'):
#                pass
    
    def set_flammable(self, f):
        """Set flammability. 0 == non-flammable, 10 == very flammable."""
        self.flammable = f
    
    # XXX implement set_fire so flammable objects can be set on fire with e.g. a fireball

    def heartbeat(self):
        pass

    def emit(self, message, ignore = []):
        """Write a message to be seen by creatures holding this Thing or in the same  
        room, skipping creatures in the list <ignore>.  See Player.perceive() for a 
        list of "perceive semantics" that can be used in emitted messages, for example
        to specify the species, gender, or proper name of a creature.  

        To avoid printing a message to certain players (for example if that player
        should receive a custom message), include them in the ignore[] list. Note that
        `Player.perceive()` will skip printing the message to any Player explicitly  
        named in the message using the &n tag. """
        if hasattr(self, 'invisible') and self.invisible == True:
            return
        # pass message to containing object, if it can receive messages
        holder = self.location
        if not holder: 
            #  this Thing is a room, pass message to all creatures in the room
            holder = self
        try:
            if holder not in ignore and hasattr(holder, 'perceive'):
                # immediate container can see messages, probably a creature/player
                dbg.debug("creature holding this object is: " + holder.id, 3)
                holder.perceive(message)
        except TypeError:
            dbg.debug("Warning, emit() called with non-list ignore parameter!", level=0)
        # now get list of recipients (usually creatures) contained by holder (usually a Room)
        recipients = [x for x in holder.contents if hasattr(x, 'perceive') and (x is not self) and (x not in ignore)]
        dbg.debug("other creatures in this room include: " + str(recipients), 3)
        for recipient in recipients:
            recipient.perceive(message)

    def move_to(self, dest, force_move=False):  
        raise  # XXX check if this code is compatible with plurals
        """Extract this object from its current location and insert into dest. 
        Returns True if the move succeeds. If the insertion fails, attempts to 
        re-insert into the original location and returns False.  
        If <force_move> is True, ignores the <fixed> attribute."""
        origin = self.location
        if self.fixed and force_move == False:
            if hasattr(self, 'is_liquid'):
                if not dest.liquid:
                    return False
            elif not hasattr(dest, 'exits'):
                return False # cannot move an object that is fixed in place
        if origin:
            origin.extract(self)
        # if cannot insert into destination, return to where it came from
        # (dest.insert returns True if insertion fails)
        if dest == None or dest.insert(self, force_insert=force_move):
            if (origin):
                origin.insert(self, force_insert=True)
            return False
        else:
            return True

    def take(self, p, cons, oDO, oIDO):
        raise  # XXX check if this code is compatible with plurals       
        if oDO == None: return "I don't know what you're trying to take!"
        if oDO != self: return "You can't take the %s!" % oDO.short_desc
        if self.fixed:  return self.fixed
        if self.location == cons.user: return "You are already holding the %s!" % self.short_desc
        if self.move_to(cons.user):
            cons.user.perceive("You take &nd%s." % self.id)
            self.emit('&nD%s takes &nd%s.' % (cons.user.id, self.id), [cons.user])
        else:
            cons.user.perceive("You cannot take &nd%s." % self.id)
        return True

    def drop(self, p, cons, oDO, oIDO):
        raise  # XXX check if this code is compatible with plurals
        if oDO != self:     return "You can't drop that!"
        if self.fixed:      return self.fixed
        if self.location != cons.user: return "You aren't holding the %s!" % self.short_desc
        if self.move_to(cons.user.location):
            cons.write("You drop the %s." % self.short_desc)
            cons.user.emit("&nD%s drops the %s." % (cons.user.id, self.short_desc))
        else:
            cons.write("You cannot drop the %s" % self.short_desc)
        return True

    def look_at(self, p, cons, oDO, oIDO):  
        '''Print out the long description of the thing.'''
        if self == oDO or self == oIDO:
            cons.write(self.long_desc)
            return True
        else:
            return "Not sure what you are trying to look at!"
        
