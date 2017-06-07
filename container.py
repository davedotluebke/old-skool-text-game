from debug import dbg
from thing import Thing
from action import Action

class Container(Thing):
    actions = []
    def __init__(self, default_name):
        Thing.__init__(self, default_name)
        self.contents = []
        self.see_inside = True      # can contents of container be seen? 
        self.closed = False         # can't remove items from closed container
        self.closed_err = ""        # custom "container is closed" error msg
        self.closable = False       # can this container be opened and closed?
        self.liquid = False         # can this container carry liquid? 
        self.max_weight_carried = 1
        self.max_volume_carried = 1
        self.insert_prepositions = ["in", "into", "inside"]
        self.actions.append(Action(self.put, ["put", "insert"], True, False))
        self.actions.append(Action(self.remove, ["remove"], True, False))
        self.actions.append(Action(self.open, ["open"], True, False))
        self.actions.append(Action(self.close_action, ["close"], True, False))

    def set_prepositions(self, *preps):
        """Set one or more appropriate prepositions for inserting an object
        into this container, each as a separate argument.
        
        For example, you put items IN or INTO a bag, but ON a table. Calling
        this function overwrites the default prepositions, which are 
        [in, into, inside]. The first preposition given will be used in messages
        and should be the most common. """
        self.insert_prepositions = list(preps)

    def insert(self, obj):
        """Put obj into this Container object, returning True if the operation failed"""
        dbg.debug("in insert")
        # error checking for max weight etc goes here
        if obj == self:
            dbg.debug('Trying to insert into self - not allowed!')
            return True
        contents_weight = 0
        contents_volume = 0
        dbg.debug("going to start looping")
        for w in self.contents:
            contents_weight = contents_weight + w.weight
            contents_volume = contents_volume + w.volume
        dbg.debug("done looping - carrying %d weight and %d volume" % (contents_weight, contents_volume))
        if self.max_weight_carried >= contents_weight+obj.weight and self.max_volume_carried >= contents_volume+obj.volume:
            dbg.debug("%s has room for %s's %d weight and %d volume" % (self.id, obj.id, obj.weight, obj.volume))
            obj.set_location(self)   # make this container the location of obj
            self.contents.append(obj)
            return False
        else:
            dbg.debug("The weight(%d) and volume(%d) of the %s can't be held by the %s, "
                  "which can only carry %d grams and %d liters (currently "
                  "holding %d grams and %d liters)" 
                  % (obj.weight, obj.volume, obj.id, self.id, self.max_weight_carried, self.max_volume_carried, contents_weight, contents_volume))
            return True
    
    def set_max_weight_carried(self, max_grams_carried):
        self.max_weight_carried = max_grams_carried

    def set_max_volume_carried(self, max_liters_carried):
        self.max_volume_carried = max_liters_carried

    def extract(self, obj):
        """Remove obj from this Container, returning True if the operation failed"""
        if obj not in self.contents:
            dbg.debug("Error! "+str(self)+" doesn't contain item "+str(obj.id))
            return True
        
        found = -1
        for i in range(0, len(self.contents)):
            if obj == self.contents[i]:
                found = i
                break
        assert found != -1
        del self.contents[i]

    def look_at(self, p, cons, oDO, oIDO):
        dbg.debug("Called Container.look_at()")
        result = Thing.look_at(self, p, cons, oDO, oIDO)
        if result != True:
            return result
        if self.see_inside:
            if self.contents:
                if self.plural:
                    pass
                preamble = "%s the %s there is:" % (self.insert_prepositions[0], self)
                cons.write(preamble.capitalize())
                for item in self.contents:
                    cons.write("a " + item.short_desc)
            else:
                if self.plural:
                    cons.write('They are empty. ')
                else:
                    cons.write("It is empty. ")
        if self.closed:
            if self.plural:
                cons.write('They are closed. ')
            else:
                cons.write("It is closed. ")
        return True
    
    def close_action(self, p, cons, oDO, oIDO):
        """Close this container, hiding the contents from view."""
        if oDO != self:
            return "Did you mean to close the %s?" % self.short_desc 
        if not self.closable:
            return "The %s can't be closed!" % self.short_desc
        if self.closed:
            cons.write("The %s is already closed!" % self.short_desc)
        else:
            cons.write("You close the %s." % self.short_desc)
            self.emit("%s closes the %s." % (cons.user.short_desc, self.short_desc), [cons.user])
            self.close()
        return True
    
    def close(self):
            self.closed = True
            self.see_inside = False
            if "closed" not in self.short_desc:
                self.short_desc = "closed " + self.short_desc

    
    def open(self, p, cons, oDO, oIDO):
        """Open this container, revealing the contents."""
        if oDO != self:
            return "Did you mean to open the %s?" % self.short_desc
        if not self.closable: 
            return "The %s can't be opened!" % self.short_desc
        if self.closed:
            if "closed" in self.short_desc:
                (head, sep, tail) = self.short_desc.partition("closed ")
                self.short_desc = head + tail
            cons.write("You open the %s." % self.short_desc)
            self.emit("%s opens the %s." % (cons.user.short_desc, self.short_desc), [cons.user])
            self.closed = False
            self.see_inside = True
        else: 
            cons.write("The %s is already open!" % self.short_desc)
        return True

    def put(self, p, cons, oDO, oIDO):
        """Put an object <oDO> into this container <oIDO>.  Returns an error 
        message if oIDO (the indirect object) is not this Container."""
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if oDO == None or oIDO == None:
            return "What are you trying to put %s what? " % sPrep
        if oIDO != self:
            return "Did you mean to 'put' something %s the %s?" % (sPrep, self.short_desc)
        if oDO.fixed: return oDO.fixed
        if sPrep not in self.insert_prepositions:
            return "You can't put the %s %s the %s, but you can put it %s the %s." % (oDO, sPrep, self, self.insert_prepositions[0], self)
        if self.closed:
            cons.write(self.closed_err if self.closed_err else "The %s is closed; you can't put anything %s it." % (self.short_desc, self.insert_prepositions[0]))
            return True
        if oDO.move_to(self): 
            cons.write("You put the %s %s the %s." % (oDO.short_desc, sPrep, self.short_desc))
            cons.user.emit("%s puts a %s %s a %s." % (cons.user.short_desc, oDO.short_desc, sPrep, self.short_desc))
        else:
            cons.write("You cannot put the %s %s the %s.", (oDO.short_desc, sPrep, self.short_desc))
        return True            

    def remove(self, p, cons, oDO, oIDO):
        """Remove an object <oDO> from this container <oIDO>. Returns an error 
        message if oDO is not in this container."""
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if oDO == None:
            return "What are you trying to remove from the %s?" % self.short_desc
        if oIDO and oIDO is not self:
            return "Sounds like you want to remove from %s, not %s." % (oIDO.short_desc, self.short_desc)
        if oIDO and sPrep != "from":
            return "Did you mean to remove the %s FROM the %s?" % (oDO.short_desc, self.short_desc)
        if oDO not in self.contents:
            # user specified a direct object, and it's not in this container
            if oIDO == self:
                # user clearly specified remove the DO from THIS container 
                cons.write("The %s is not %s the %s!" % (oDO.short_desc, self.insert_prepositions[0], self.short_desc))
                return True
            else:
                # user didn't specify an IDO, or specified something else as IDO'
                return "The %s is not %s the %s!" % (oDO.short_desc, self.insert_prepositions[0], self.short_desc)  
        if oDO.fixed: 
            return oDO.fixed
        if oDO in cons.user.contents:
            cons.write("If you want to remove something from your own inventory, drop it.")
            return True
        if self.closed: 
            cons.write(self.closed_err if self.closed_err else "The %s is closed; you can't remove the %s." % (self.short_desc, oDO.short_desc))
        if oDO.move_to(cons.user): 
            cons.write("You remove the %s from the %s." % (oDO.short_desc, self.short_desc))
            cons.user.emit("%s removes a %s from a %s" % (cons.user.short_desc, oDO.short_desc, self.short_desc))
        else:
            cons.write("You cannot remove the %s from the %s" % (oDO.short_desc, self.short_desc))
        return True