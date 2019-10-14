from debug import dbg
from action import Action
import random
import copy
import gametools

class Thing(object):
    ID_dict = {}
    game = None

    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, default_name, path, pref_id=None, plural_name=None):
        self.unlisted = False # should this thing be listed in room description  
        self.path = gametools.findGamePath(path) if path else None
        self.versions = {gametools.findGamePath(__file__): 3}
        self.names = [default_name]
        self.plural_names = [default_name+'s' if not plural_name else plural_name]
        self._add_ID(default_name if not pref_id else pref_id)
        self.plurality = 1  # how many identical objects this Thing represents
        self._weight = 0.0
        self._volume = 0.0
        self._value = 0
        self.emits_light = False
        self.flammable = 0
        self.location = None
        self.fixed = False          # False if unfixed, error message if fixed 
        self._short_desc = 'need_short_desc'
        self._plural_short_desc = 'need_plural_short_desc'
        self._long_desc = 'need_long_desc'
        self.adjectives = set()
        self.contents = None        # None - only Containers can contain things
        self.spawn_location = None
        self.spawn_interval = None
        self.spawn_message = None

    def __del__(self):
        dbg.debug('Deleting object: %s: %s.' % (self.names[0], self.id))

    def __str__(self): 
        return self.names[0]

    #
    # INTERNAL USE METHODS (i.e. _method(), not imported)
    #
    def _add_ID(self, preferred_id, remove_existing=False):
        """Add object to Thing.ID_dict (the dictionary mapping IDs to objects).

        Takes a preferred ID string and (if necessary) creates a unique ID
        string from it. Returns the unique ID string. If <remove_existing> is
        set to True, first attempts to delete this object's current ID from 
        Thing.ID_dict (useful for assigning new IDs to existing objects)"""
        if remove_existing:
            try:
                del Thing.ID_dict[self.id]
            except AttributeError:
                dbg.debug('%s has no id attribute!' % self)
            except KeyError:
                dbg.debug('%s.id was not in Thing.ID_dict!' % self)
        self.id = preferred_id
        while self.id in Thing.ID_dict:     # unique-ify self.id if necessary
            self.id = self.id + str(random.randint(0, 9))
        Thing.ID_dict[self.id] = self
        return self.id

    def _change_objs_to_IDs(self):
        """Replace object references with ID strings, in preparation for pickling."""
        if self.location:
            self.location = self.location.id
        if self.contents:
            self.contents = [obj.id for obj in self.contents]

    def _restore_objs_from_IDs(self):
        """Update object references stored as ID strings to directly reference the objects, using Thing.ID_dict."""
        if isinstance(self.location, str):
            self.location = Thing.ID_dict[self.location] # XXX will this work correctly for the room if it isn't loaded yet? 
        if self.contents != None:
            self.contents = [Thing.ID_dict[id] for id in self.contents if (isinstance(id, str) and id in Thing.ID_dict)]

    #
    # SET/GET METHODS (methods to set or query attributes)
    #
    def add_names(self, *sNames):
        """Add one or more strings as possible noun names for this object, each as a separate argument"""
        self.names += list(sNames)

    def add_plural_names(self, *sPluralNames):
        """Add one or more strings as possible plural noun names for this object, each as a separate argument"""
        self.plural_names += list(sPluralNames)

    def add_adjectives(self, *sAdjs):
        """Add one or more adjective strings, each as a separate argument"""
        self.adjectives |= set(sAdjs)
    
    def remove_adjectives(self, *sAdjs):
        """Remove one or more adjective strings, each specified as a separate argument. 
        Ignores any adjectives that are not associated with the object."""
        self.adjectives -= set(sAdjs)

    def set_weight(self, grams):
        if (grams < 0):
            dbg.debug("Error: weight cannot be negative")
            raise
        else:
            self._weight = grams
    
    def get_weight(self):
        '''Return the weight of a single object times the number of objects present'''
        return self._weight * self.plurality

    def set_volume(self, liters):
        if (liters < 0):
            dbg.debug("Error: volume cannot be negative")
            raise
        else:
            self._volume = liters
    
    def get_volume(self):
        '''Return the volume of a single object times the number of objects present'''
        return self._volume * self.plurality

    def set_location(self, containing_object):
        self.location = containing_object

    def fix_in_place(self, error_message):
        self.fixed = error_message

    def unfix(self):
        self.fixed = False

    def set_description(self, s_desc, l_desc, p_s_desc=None, unlisted=False):
        self._short_desc = s_desc
        self._long_desc = l_desc
        self._plural_short_desc = p_s_desc if p_s_desc else s_desc+"s"
        self.unlisted = unlisted

    def set_flammable(self, f):
        """Set flammability. 0 == non-flammable, 10 == very flammable."""
        self.flammable = f

    def get_total_value(self):
        """Return the value of the thing as an integer. 
        The value returned will be multiplied by the plurality of the object.
        Can be overloaded for more complicated functionality."""
        return self.get_unit_value() * self.plurality
    
    def get_unit_value(self):
        """Return the value of the thing as an integer.
        The value returned will NOT be multiplied by the plurality of the object.
        Can be overloaded for more complicated functionality."""
        return self._value

    def set_value(self, value):
        """Set the value of the thing. Value must be an integer. 
        Can be overloaded for more complicated functionality."""
        self._value = value
    
    # XXX implement set_fire so flammable objects can be set on fire with e.g. a fireball

    def get_short_desc(self, perceiver=None, definite=False, indefinite=False):
        '''Return the short description of this object, optionally prepended
        by an article. Prepends with 'the' if <definite> is True, or with 'a'
        or 'an' if indefinite is True. Only one of definite/indefinite should 
        be set to True. The <perceiver> is the Creature (usually a Player) 
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
            return quantity + self._plural_short_desc
        else: 
            return article + self._short_desc

    def indefinite(self):
        """Return the appropriate indefinite article ('a' or 'an') to use with
        the object, based on starting character of self._short_desc. Overload  
        for objects not starting with a vowel that should still use 'an'"""
        return "an" if self._short_desc[0] in 'aeiou' else "a"

    def possessive(self):
        """Return 'his', 'her', 'their', or 'its' as appropriate."""
        if hasattr(self, 'gender'):
            if self.gender == 'male': 
                return 'his'
            elif self.gender == 'female':
                return 'her'
            elif self.gender == 'non-binary':
                return 'their'
        # other gender or no gender specified:
        return 'its'  

    def pronoun(self):
        """Return 'he', 'she', or 'it' as appropriate."""
        if hasattr(self, 'gender'):
            if self.gender == 'male': 
                return 'he'
            elif self.gender == 'female':
                return 'she'
            elif self.gender == 'non-binary':
                return 'their'
        # other gender or no gender specified:
        return 'it'

    #
    # OTHER EXTERNAL METHODS (misc externally visible methods)
    #
    def heartbeat(self):
        pass

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
        if state.get("actions"):
            del state["actions"]
        default_obj = gametools.clone(self.path)
        default_state = default_obj.__dict__
        for attr in list(state):
            if attr not in default_state or \
               state[attr] != default_state[attr] or \
               attr == 'path' or attr == 'version_number' \
               or attr == 'versions':
                saveable[attr] = state[attr]
        default_obj.destroy()
        if 'adjectives' in saveable and isinstance(saveable['adjectives'], set):
            saveable['adjectives'] = list(saveable['adjectives'])
        return saveable

    def replicate(self):
        """Make a copy of an object and register in Thing.ID_dict[]. Does not affect
        the source or destination plurality field, and does not register a heartbeat
        function for the copy. The calling function should handle these effects."""
        if self.contents:
            raise Exception("Can't replicate containers with anything inside!")
        new_obj = copy.copy(self)
        # Resolve fields that require special treatment
        new_obj._add_ID(new_obj.id)
        new_obj.location = None  # hasn't been properly added to container yet
        new_obj.move_to(self.location, merge_pluralities=False)
        return new_obj
    
    def is_identical_to(self, obj):
        """Compares self with obj, ignoring the plurality and id fields. Return
        True if self is otherwise identical to obj, False if they differ. 
        To avoid deep comparisons, containers with a non-empty `contents` list
        always return False."""
        if self.contents:
            return False
        # keep track of target plurality & id, but temporarily
        # set equal to source plurality for easy comparison
        tmp = (obj.plurality, obj.id)
        obj.plurality, obj.id = self.plurality, self.id
        if self.__dict__ == obj.__dict__:
            obj.plurality, obj.id = tmp
            return True
        else:
            obj.plurality, obj.id = tmp
            return False
    
    def destroy(self):
        """Removes and object from Thing.ID_dict, extracts it, and deregisters its heartbeat."""
        try:
            del Thing.ID_dict[self.id]
        except KeyError:
            dbg.debug('%s was already moved from Thing.ID_dict' % self, 2)
        if self.location:
            self.location.extract(self)
            self.location = None
        if self in Thing.game.heartbeat_users:
            Thing.game.deregister_heartbeat(self)

    def update_obj(self, saveable):
        """Return the updated object from the "saveable" version created above. 
        Also call update_version() to make sure that all objects are up to date."""
        state = self.__dict__.copy()
        for attr in list(saveable):
            state[attr] = saveable[attr]

        self.__dict__.update(state)

        self.update_version()

    def update_version(self):
        """Updates the version of the object, and runs snipets of code to make 
        sure all objects will still function."""
        if not hasattr(self, 'versions') and not hasattr(self, 'version_number'):
            self.version_number = 1
        
        if hasattr(self, 'version_number') and self.version_number < 2:
            try:
                if 'short_desc' in self.__dict__:
                    self._short_desc = self.short_desc
                    del self.__dict__['short_desc']
                if 'long_desc' in self.__dict__:
                    self._long_desc = self.long_desc
                    del self.__dict__['long_desc']
                self.version_number = 2
            except KeyError:
                dbg.debug('Error updating object %s in Thing.update_version()' % self)
        
        if hasattr(self, 'version_number'):
            # Changing to dictionary-based versioning system
            self.versions[gametools.findGamePath(__file__)] = 3
            del self.__dict__['version_number']

    def delete(self):
        if self.contents:
            for i in self.contents:
                i.delete()
        if self.location:
            self.location.extract(self)
        del Thing.ID_dict[self.id]

    def emit(self, message, ignore = []):
        """Write a message to be seen by creatures holding this Thing or in the same  
        room, skipping creatures in the list <ignore>.  See Player.perceive() for a 
        list of "perceive semantics" that can be used in emitted messages, for example
        to specify the species, gender, or proper name of a creature.  

        To avoid printing a message to certain players (for example if that player
        should receive a custom message), include them in the ignore[] list. 
        NOTE: `Player.perceive()` will skip printing the message to any Player   
        explicitly named in the message using the &n tag. """
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
                dbg.debug("creature holding this object is: " + holder.id, 4)
                holder.perceive(message)
        except TypeError:
            dbg.debug("Warning, emit() called with non-list ignore parameter!")
        # now get list of recipients (usually creatures) contained by holder (usually a Room)
        recipients = [x for x in holder.contents if hasattr(x, 'perceive') and (x is not self) and (x not in ignore)]
        dbg.debug("other creatures in this room include: " + str(recipients), 4)
        for recipient in recipients:
            recipient.perceive(message)

    def move_to(self, dest, force_move=False, merge_pluralities=True):  
        """Extract this object from its current location and insert into dest. 
        Returns True if the move succeeds. If the insertion fails, attempts to 
        re-insert into the original location and returns False.  
        If <force_move> is True, ignores the <fixed> attribute.
        If <merge_pluralities is True, checks if this object is identical to any 
        objects currently in dest.contents; if so, merges them into a plurality.
        Note that the parser would have already split off the object from a 
        plurality in the origin, if necessary."""
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
        if dest == None or dest.insert(self, force_insert=force_move, merge_pluralities=merge_pluralities):
            if (origin):
                origin.insert(self, force_insert=True, merge_pluralities=True)
            return False
        else:
            return True

    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    #
    def take(self, p, cons, oDO, oIDO):
        if oDO == None: 
            return "I don't know what you're trying to take!"
        # get description before calling move_to(), which can change plurality.
        # Want short desc with definite article as perceived by this player 
        description = cons.user.perceive('&nd'+self.id, silent = True)  
        if oDO != self: 
            return "You can't take %s!" % description
        if self.fixed: 
            return self.fixed
        if self.location == cons.user: 
            return "You are already holding %s!" % description
        if self.move_to(cons.user):
            cons.user.perceive("You take %s." % description)
            self.emit('&nD%s takes &nd%s.' % (cons.user.id, self.id), [cons.user])
        else:
            cons.user.perceive("You cannot take %s." % description)
        return True

    def drop(self, p, cons, oDO, oIDO):
        # get description before calling move_to(), which can change plurality.
        # Want short desc with definite article as perceived by this player 
        description = cons.user.perceive('&nd'+self.id, silent = True)  
        if oDO != self:
            return "You can't drop that!"
        if self.fixed:
            return self.fixed
        if self.location != cons.user: 
            return "You aren't holding  %s!" % description
        if self.move_to(cons.user.location):
            cons.user.perceive("You drop %s." % description)
            cons.user.emit("&nD%s drops %s." % (cons.user.id, description))
        else:
            cons.write("You cannot drop %s" % description)
        return True

    def look_at(self, p, cons, oDO, oIDO):
        '''Print out the long description of the thing.'''
        if self == oDO or self == oIDO:
            cons.user.perceive(self._long_desc)
            return True
        else:
            return "Not sure what you are trying to look at!"

    actions = {}
    actions["look"] = Action(look_at, True, False)
    actions["examine"] = Action(look_at, True, False)
    actions["take"] = Action(take, True, False)
    actions["get"] = Action(take, True, False)
    actions["drop"] = Action(drop, True, False)


dbg.ID_dict = Thing.ID_dict # Allow the DebugLog to access Thing.ID_dict
