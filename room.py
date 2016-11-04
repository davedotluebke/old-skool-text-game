from debug import dbg
from container import Container
from action import Action

class Room(Container):
    def __init__(self, ID):
        Container.__init__(self, ID)
        self.exits = {}
        self.set_max_weight_carried(4e9)
        self.set_max_volume_carried(3e9)
        self.actions.append(Action(self.go_to, ["go", "walk"], True, False))
        self.fix_in_place("You can't move that!")

    def add_exit(self, exit_name, exit_room):
        self.exits[exit_name] = exit_room
    
    def look_at(self, p, cons, oDO, oIDO):
        """Print long description of room, list items (excluding this player) and exits"""
        cons.write(self.long_desc)
        assert(cons.user in self.contents)  # current player should always be in the room 
        contents_minus_user = [i for i in self.contents if i is not cons.user]  
        dbg.debug("self.contents = %s" % (self.contents))
        dbg.debug("contents_minus_user = %s" % (contents_minus_user))

        if len(contents_minus_user) > 0:
            cons.write("Here you see:")
            for item in contents_minus_user:
                cons.write(item.short_desc)
        cons.write('Exits are:')
        for e in self.exits:
            cons.write(e)
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
            cons.write("You %s to the %s into the %s." % (words[0], sExit, dest.id))
            if cons.user.move_to(dest):
                cons.write("You enter %s." % cons.user.location.short_desc)
                cons.write("exits are:")
                for w in cons.user.location.exits:
                    cons.write(w)
                return True
            else:
                return "For some reason you are unable to go to the %s." % sExit
        else: # user did not specify a valid exit
            return "I don't see how to go %s!" % sExit
