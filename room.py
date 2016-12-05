from debug import dbg
from container import Container
from action import Action

class Room(Container):
    def __init__(self, default_name, light=1):
        """Initialize the room. Set <light> level to 0 for a dark room."""
        Container.__init__(self, default_name)
        self.exits = {}
        self.set_max_weight_carried(4e9)
        self.set_max_volume_carried(3e9)
        self.actions.append(Action(self.go_to, ["go", "walk"], True, False))
        self.actions.append(Action(self.look_at, ["look", "examine"], True, True))
        self.fix_in_place("You can't move that!")
        self.closable = False
        self.light = light  # Can see and perceive emits when light level > 0

    def add_exit(self, exit_name, exit_room):
        self.exits[exit_name] = exit_room
         
    def is_dark(self):
        return False if self.light > 0 else True
        
    def insert(self, obj):
        if Container.insert(self, obj):
            return True  # insert returns True if operation failed
        
        # insert succeeded; see if obj is or contains a light source
        possible_lights = [obj]
        for i in possible_lights:
            self.light += i.emits_light  # i.emits_light is positive if object emits light, else 0
            if hasattr(i, "see_inside") and i.see_inside: 
                possible_lights += i.contents # recurse on i.contents
        return False
        
    def extract(self, obj):
        if Container.extract(self, obj): 
            return True  # extract returns True if the operation failed
        
        # extract succeeded; see if obj is or contains a light source
        possible_lights = [obj]
        for i in possible_lights:
            self.light -= i.emits_light  # i.emits_light is positive if object emits light, else 0
            if hasattr(i, "see_inside") and i.see_inside:
                possible_lights += i.contents
        return False

    def look_at(self, p, cons, oDO, oIDO):
        """Print long description of room, list items (excluding this player) and exits"""
        dbg.debug("Called Room.look_at()")
        # if verb is transitive, verify that the room is the direct object
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if sDO and (oDO is None): 
            return "I'm not sure what you are trying to look at!"
        if self.is_dark():
            cons.write("It's too dark to see anything here.")
            return True
        cons.write(self.long_desc)
        assert(cons.user in self.contents)  # current player should always be in the room 
        contents_minus_user = [i for i in self.contents if i is not cons.user]  
        dbg.debug("self.contents = %s" % (self.contents))
        dbg.debug("contents_minus_user = %s" % (contents_minus_user))

        if len(contents_minus_user) > 0:
            cons.write("Here you see:")
            for item in contents_minus_user:
                cons.write("\ta " + item.short_desc)
        cons.write('Exits are:')
        for e in self.exits:
            cons.write('\t' + e)
        return True

    def move_to(self, p, cons, oDO, oIDO):
        cons.write('rooms cannot be moved!')

    def go_to(self, p, cons, oDO, oIDO):
        words = p.words
        dbg.debug("verb function go_to: words == ")
        dbg.debug(str(words))
        sExit = words[1]
        if sExit in list(self.exits):
            dest = self.exits[sExit]
            cons.write("You %s to the %s." % (words[0], sExit))
            if cons.user.move_to(dest):
                if dest.is_dark():
                    cons.write("It's too dark to see anything here.")
                    return True
                cons.write("You enter a %s." % cons.user.location.short_desc)
                if (len(cons.user.location.exits) > 0):
                    cons.write("Exits are:")
                    for w in cons.user.location.exits:
                        cons.write('\t' + w)
                else:
                    cons.write("There are no obvious exits.")
                return True
            else:
                return "For some reason you are unable to go to the %s." % sExit
        else: # user did not specify a valid exit
            return "I don't see how to go %s!" % sExit
