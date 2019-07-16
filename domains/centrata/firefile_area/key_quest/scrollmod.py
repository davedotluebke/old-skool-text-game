import gametools
import thing

class Scroll(thing.Thing):
    def __init__(self, default_name, path, short_desc, long_desc, message, pref_id=None):
        super().__init__(default_name, path)
        self.set_description(short_desc, long_desc)
        self.actions.append(thing.Action(self.read, ['read'], True, False))
        self.message = message
    
    def read(self, p, cons, oDO, oIDO):
        cons.user.perceive('You read: %s' % self.message)
        return True
