from container import *

class Room(Container):
    def __init__(self, ID):
        Container.__init__(self, ID)
        self.exits = {}
        self.set_max_weight_carried(4e9)
        self.set_max_volume_carried(3e9)
        self.verb_dict["go"]        = self.go_to
        self.verb_dict["walk"]      = self.go_to

    def add_exit(self, exit_name, exit_room):
        self.exits[exit_name] = exit_room

    def look_at(self, cons, oDO, oIDO):
        Container.look_at(self, cons, oDO, oIDO)
        cons.write('exits are:')
        for e in self.exits:
            cons.write(e)

    def move_to(self, cons, oDO, oIDO):
        cons.write('rooms cannot be moved into %s!' % oIDO.id)

    def go_to(self, cons, oDO, oIDO):
        words = cons.words
        cons.debug("verb function go_to: words == ")
        cons.debug(words)
        sExit = words[1]
        if sExit in list(self.exits):
            dest = self.exits[sExit]
            cons.write("You %s to the %s into the %s." % (words[0], sExit, dest.id))
            cons.user.move_to(cons, dest, None)
            cons.write("You enter %s." % cons.user.location.short_desc)
            cons.write("exits are:")
            for w in cons.user.location.exits:
                cons.write(w)