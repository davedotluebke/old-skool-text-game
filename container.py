from debug import dbg
from thing import Thing
from action import Action
import gametools

class Container(Thing):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, default_name, path, pref_id=None):
        Thing.__init__(self, default_name, path, pref_id)
        self.contents = []
        self.see_inside = True      # can contents of container be seen? 
        self.liquid = False         # can this container carry liquid? 
        self.closable = False       # can this container be opened and closed?
        self.closed = False         # can't remove items from closed container
        self.closed_err = ""        # custom "container is closed" error msg
        self.max_weight_carried = 1
        self.max_volume_carried = 1
        self.insert_prepositions = ["in", "into", "inside"]
        self.versions[gametools.findGamePath(__file__)] = 1

    #
    # INTERNAL USE METHODS (i.e. _method(), not imported)
    #

    #
    # SET/GET METHODS (methods to set or query attributes)
    #
    def set_prepositions(self, *preps):
        """Set one or more appropriate prepositions for inserting an object
        into this container, each as a separate argument.
        
        For example, you put items IN or INTO a bag, but ON a table. Calling
        this function overwrites the default prepositions, which are 
        [in, into, inside]. The first preposition given will be used in messages
        and should be the most common. """
        self.insert_prepositions = list(preps)

    def set_spawn(self, path, interval):
        g = Thing.game
        g.events.schedule(g.time+interval, self.spawn_obj, (path, interval, g))

    def set_max_weight_carried(self, max_grams_carried):
        self.max_weight_carried = max_grams_carried

    def set_max_volume_carried(self, max_liters_carried):
        self.max_volume_carried = max_liters_carried

    #
    # OTHER EXTERNAL METHODS (misc externally visible methods)
    #
    def detach(self, container_path):
        '''Remove the container from Thing.ID_dict[] and moves all objects in the container
        to nulspace (this removes references to the container instance, specifically
        the location field of contained objects). This should be called preparatory
        to deleting or reloading the container.

        Returns True for success or False if the container is not in Thing.ID_dict[]'''
        try:
            container = Thing.ID_dict[container_path]
            for o in container.contents:
                o.move_to(Thing.ID_dict['nulspace'], force_move=True)
            del Thing.ID_dict[container_path]
            return True
        except KeyError:
            return False
    
    def insert(self, obj, force_insert=False, merge_pluralities=True):
        """Put obj into this Container object, returning True if the operation failed. 
        If <force_insert> is True, ignore weight and volume limits."""
        # error checking for max weight etc goes here
        if obj is self:
            dbg.debug('Trying to insert into self - not allowed!', 0)
            return True
        if obj == None:
            dbg.debug('Trying to insert a null object into %s!' % self, 0)
            return True
        if obj.id not in Thing.ID_dict and force_insert == False:
            dbg.debug("Now returns True when an object's id not in Thing.ID_dict", 0)
            return True
        contents_weight = 0.0
        contents_volume = 0.0
        for w in self.contents:
            contents_weight = contents_weight + w.get_weight()
            contents_volume = contents_volume + w.get_volume()
        dbg.debug("insert(): %s currently carrying %d weight and %d volume" % (self.id, contents_weight, contents_volume), 3)
        if (force_insert == True) or (self.max_weight_carried >= contents_weight+obj.get_weight() and self.max_volume_carried >= contents_volume+obj.get_volume()):
            dbg.debug("%s has room for %s's %d weight and %d volume" % (self.id, obj.id, obj.get_weight(), obj.get_volume()), 3)
            # Success! The object fits in the container, add it.  
            self.contents.append(obj)
            obj.set_location(self)   # make this container the location of obj
            # If an identical object already exists in the container, instead increase its plurality count and destroy obj.
            if merge_pluralities:
                for w in self.contents:
                    if (w is not obj) and obj.is_identical_to(w):
                        obj.plurality += w.plurality 
                        w.destroy()
                        break
            return False
        else:
            dbg.debug("The weight(%d) and volume(%d) of the %s can't be held by the %s, "
                  "which can only carry %d grams and %d liters (currently "
                  "holding %d grams and %d liters)" 
                  % (obj.get_weight(), obj.get_volume(), obj.id, self.id, self.max_weight_carried, self.max_volume_carried, contents_weight, contents_volume), 2)
            return True

    def extract(self, obj):
        """Remove obj (which may be plural) from this Container, returning 
        the extracted object or returning True if the operation failed."""
        # TODO: raise exceptions specific to "object not found" or "not enough objects"

        if obj not in self.contents:
            dbg.debug("Error! "+str(self)+" doesn't contain item "+str(obj.id), 0)
            return True
        
        i = self.contents.index(obj)  # no need for try..except since we already know obj in list
        del self.contents[i]
        return obj

    def close(self):
            self.closed = True
            self.see_inside = False
            if "closed" not in self._short_desc:
                self._short_desc = "closed " + self._short_desc

    def spawn_obj(self, info):
        path = info[0]
        interval = info[1]
        game = info[2]
        g = Thing.game
        g.events.schedule(game.time+interval, self.spawn_obj, (path, interval, game))
        for i in self.contents:
            if i.path == path:
                return
        import path as obj_file
        obj = obj_file.clone()
        self.insert(obj)

    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    #
    def look_at(self, p, cons, oDO, oIDO):
        result = Thing.look_at(self, p, cons, oDO, oIDO)
        if result != True:
            return result
        if self.see_inside:
            if self.contents:
                preamble = "%s the %s there is:" % (self.insert_prepositions[0], self)
                cons.write(preamble.capitalize())
                for item in self.contents:
                    cons.write(item.get_short_desc(indefinite=True))
            else:
                cons.write("It is empty. ")
        if self.closed:
            cons.write("It is closed. ")
        return True
    
    def close_action(self, p, cons, oDO, oIDO):
        """Close this container, hiding the contents from view."""
        if oDO != self:
            return "Did you mean to close the %s?" % self._short_desc 
        if not self.closable:
            return "The %s can't be closed!" % self._short_desc
        if self.closed:
            cons.write("The %s is already closed!" % self._short_desc)
        else:
            cons.write("You close the %s." % self._short_desc)
            self.emit("&nD%s closes the %s." % (cons.user.id, self._short_desc), [cons.user])
            self.close()
        return True

    def open_action(self, p, cons, oDO, oIDO):
        """Open this container, revealing the contents."""
        if oDO != self:
            return "Did you mean to open the %s?" % self._short_desc
        if not self.closable: 
            return "The %s can't be opened!" % self._short_desc
        if self.closed:
            if "closed" in self._short_desc:
                (head, sep, tail) = self._short_desc.partition("closed ")
                self._short_desc = head + tail
            cons.write("You open the %s." % self._short_desc)
            self.emit("&nD%s opens the %s." % (cons.user.id, self._short_desc), [cons.user])
            self.closed = False
            self.see_inside = True
        else: 
            cons.write("The %s is already open!" % self._short_desc)
        return True

    def put(self, p, cons, oDO, oIDO):
        """Put an object <oDO> into this container <oIDO>.  Returns an error 
        message if oIDO (the indirect object) is not this Container."""
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if oDO == None or oIDO == None:
            return "What are you trying to put %s what? " % sPrep
        if oIDO != self:
            return "Did you mean to 'put' something %s the %s?" % (sPrep, self._short_desc)
        if oDO.fixed: return oDO.fixed
        if sPrep not in self.insert_prepositions:
            return "You can't put the %s %s the %s, but you can put it %s the %s." % (oDO, sPrep, self, self.insert_prepositions[0], self)
        if self.closed:
            cons.write(self.closed_err if self.closed_err else "The %s is closed; you can't put anything %s it." % (self._short_desc, self.insert_prepositions[0]))
            return True
        if oDO.move_to(self): 
            cons.write("You put the %s %s the %s." % (oDO._short_desc, sPrep, self._short_desc))
            cons.user.emit("&nD%s puts a %s %s a %s." % (cons.user.id, oDO._short_desc, sPrep, self._short_desc))
        else:
            cons.write("You cannot put the %s %s the %s.", (oDO._short_desc, sPrep, self._short_desc))
        return True            

    def remove(self, p, cons, oDO, oIDO):
        """Remove an object <oDO> from this container <oIDO>. Returns an error 
        message if oDO is not in this container."""
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if oDO == None:
            return "What are you trying to remove from the %s?" % self._short_desc
        if oIDO and oIDO is not self:
            return "Sounds like you want to remove from %s, not %s." % (oIDO._short_desc, self._short_desc)
        if oIDO and sPrep != "from":
            return "Did you mean to remove the %s FROM the %s?" % (oDO._short_desc, self._short_desc)
        if oDO not in self.contents:
            # user specified a direct object, and it's not in this container
            if oIDO == self:
                # user clearly specified remove the DO from THIS container 
                cons.write("The %s is not %s the %s!" % (oDO._short_desc, self.insert_prepositions[0], self._short_desc))
                return True
            else:
                # user didn't specify an IDO, or specified something else as IDO'
                return "The %s is not %s the %s!" % (oDO._short_desc, self.insert_prepositions[0], self._short_desc)  
        if oDO.fixed: 
            return oDO.fixed
        if oDO in cons.user.contents:
            cons.write("If you want to remove something from your own inventory, drop it.")
            return True
        if self.closed: 
            cons.write(self.closed_err if self.closed_err else "The %s is closed; you can't remove the %s." % (self._short_desc, oDO._short_desc))
        if oDO.move_to(cons.user): 
            cons.write("You remove the %s from the %s." % (oDO._short_desc, self._short_desc))
            cons.user.emit("&nD%s removes a %s from a %s" % (cons.user.id, oDO._short_desc, self._short_desc))
        else:
            cons.write("You cannot remove the %s from the %s" % (oDO._short_desc, self._short_desc))
        return True

    actions = dict(Thing.actions)
    actions["look"] =    Action(look_at, True, False)
    actions["examine"] = Action(look_at, True, False)
    actions["put"] =     Action(put, True, False)
    actions["insert"] =  Action(put, True, False)
    actions["remove"] =  Action(remove, True, False)
    actions["open"] =    Action(open_action, True, False)
    actions["close"] =   Action(close_action, True, False)
