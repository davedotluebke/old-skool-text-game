import gametools
import thing

class Scroll(thing.Thing):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, default_name, path, short_desc, long_desc, message, pref_id=None):
        super().__init__(default_name, path)
        self.set_description(short_desc, long_desc)
        self.message = message

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
    
    def read(self, p, cons, oDO, oIDO):
        cons.user.perceive('You read: %s' % self.message)
        return True

    actions = dict(Thing.actions)  # make a copy, don't change Thing's dict!
    actions['read'] = Action(read, True, False)
