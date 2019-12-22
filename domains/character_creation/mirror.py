import thing
import gametools
import action

class Mirror(thing.Thing):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, mirror_quality, what_you_see, exit_room, species=None, gender=None, adj1=None, adj2=None):
        super().__init__('mirror', __file__)
        self.set_description('%s mirror' % mirror_quality, 'In this %s mirror you see %s.' % (mirror_quality, what_you_see))
        self.add_adjectives(mirror_quality)
        self.dest = exit_room
        self.species = species
        self.gender = gender
        self.adj1 = adj1
        self.adj2 = adj2

    #
    # INTERNAL USE METHODS (i.e. _method(), not imported)
    #

    #
    # SET/GET METHODS (methods to set or query attributes)
    #

    #
    # OTHER EXTERNAL METHODS (misc externally visible methods)
    #

    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    #
    def look_at(self, p, cons, oDO, oIDO):
        if self == oDO or self == oIDO:
            if self.adj2:
                cons.user.perceive("In this mirror you see a "+self.adj1+" "+self.adj2+" "+cons.user.gender+" "+cons.user.species)
            else:
                cons.user.perceive(self._long_desc)
            return True
        else:
            return "Not sure what you are trying to look at!"

    def enter(self, p, cons, oDO, oIDO):
        dest = gametools.load_room(self.dest)
        if self.dest == gametools.DEFAULT_START_LOC:
            scroll = gametools.clone('domains.school.scroll')
            scroll.user = cons.user
            scroll.move_to(cons.user)
            thing.Thing.game.register_heartbeat(scroll)
            cons.user.set_start_loc(dest)

        if cons.user.move_to(dest) == False:
            return "Error! You attempt to enter the mirror but encounter a glitch in the space-time continuum. Please report an error."

        label = ""  # construct a label, e.g. "swarthy young male gnome"
        if self.adj1:
            label += self.adj1 + " "
            cons.user.adj1 = self.adj1
            cons.user.add_adjectives(self.adj1)
        elif cons.user.adj1:
            label += cons.user.adj1 + " "
        else:
            label = "nondescript" + " "
        if self.adj2:   
            label += self.adj2 + " "
            cons.user.adj2 = self.adj2
            cons.user.add_adjectives(self.adj2)
        elif cons.user.adj2:
            label += cons.user.adj2 + " "
        if self.gender:
            label += self.gender + " "
            cons.user.add_adjectives(self.gender)
            cons.user.gender = self.gender
        elif cons.user.gender:
            label += cons.user.gender + " "
        if self.species:
            label += self.species
            cons.user.species = self.species
            cons.user.add_names(self.species)
        elif cons.user.species:
            label += cons.user.species + " "
        cons.user.set_description(label, "A " + label)

        cons.user.perceive("As if in a dream, you approach the mirror and enter it, the glass parting like gauze "
            "to let you through. Somehow you feel more sharply defined, more real! You notice your surroundings "
            "have changed...\n")
        dest.report_arrival(cons.user)
        return True

    actions = dict(thing.Thing.actions)  # make a copy, don't change Thing's dict!
    actions['enter'] =   action.Action(enter, True, False)
    actions['look'] =    action.Action(look_at, True, False)
    actions['examine'] = action.Action(look_at, True, False)
