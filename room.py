from debug import dbg
from container import Container

class Room(Container):
    def __init__(self, ID):
        Container.__init__(self, ID)
        self.exits = {}
        self.set_max_weight_carried(4e9)
        self.set_max_volume_carried(3e9)
        self.verb_dict["go"]        = self.go_to
        self.verb_dict["walk"]      = self.go_to
        del self.verb_dict["take"]
        del self.verb_dict["drop"]
        self.fixed = True
        self.hidden_exits = {}


    def add_exit(self, exit_name, exit_room):
        self.exits[exit_name] = exit_room
    
    def add_secret_exit(self, exit_name, hiding_spot, exit_room):
        self.hidden_exits['%s %s' % (exit_name, hiding_spot)] = exit_room

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
            cons.user.move_to(p, cons, dest, None)
            cons.write("You enter %s." % cons.user.location.short_desc)
            cons.write("exits are:")
            for w in cons.user.location.exits:
                cons.write(w)

    def reveal_exit(self, hiding_spot, exit_name):
        revealed_exit = self.hidden_exits['%s %s' % (exit_name, hiding_spot)]
        self.exits[exit_name] = revealed_exit
        del self.hidden_exits['%s %s' % (exit_name, hiding_spot)]
        dbg.debug('exit hidden by %s called %s leading to room %s revealed' % (hiding_spot, exit_name, revealed_exit.id()))

    def hide_exit(self, hiding_spot, exit_name):
        hiding_exit = self.exits[exit_name]
        self.hidden_exits['%s %s' % (exit_name, hiding_spot)] = hiding_exit
        del self.exits[exit_name]
