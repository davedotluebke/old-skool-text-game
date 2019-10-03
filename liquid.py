import gametools

from thing import Thing
from debug import dbg
from action import Action

from scenery import Scenery
from container import Container

class Liquid(Scenery):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, default_name, path=None, short_desc = 'need_short_desc', long_desc = 'need_long_desc', pref_id=None):
        Scenery.__init__(self, default_name, short_desc, long_desc, pref_id)
        # Scenery __init__() creates a per-object actions[] dict
        self.actions['pour'] =  Action(Liquid.pour, True, False)
        self.actions['drink'] = Action(Liquid.drink, True, False)
        self.actions['sip'] =   Action(Liquid.drink, True, False)
        self.actions['taste'] = Action(Liquid.drink, True, False)
        self.is_liquid = True
        self.path = gametools.findGamePath(path) if path else None
        self.versions[gametools.findGamePath(__file__)] = 1

    #
    # ACTION METHODS (dictionary for scenery defined per-object)
    # 
    def pour(self, p, cons, oDO, oIDO):
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        loc = self.location
        if oDO == loc: 
            # e.g. allow user to type "pour flask" instead of "pour potion"
            oDO = self
        if sPrep == "out":
            if (oDO, oIDO) == (self, None) or (oDO, oIDO) == (None, self):
                # e.g. "pour out potion" or "pour potion out"
                cons.write("You pour out the %s on the ground." % self)
                cons.user.emit("&nD%s pours something on the ground." % cons.user.id)
                self.destroy()
                # TODO: actually delete the object
                return True
        if oDO == self and sPrep in ("in", 'into') and isinstance(oIDO, Container) and oIDO.liquid:
            if loc.extract(self):
                cons.write("You can't get the %s out of the %s!" % (self, loc))
                return True
            if oIDO.insert(self):
                cons.write("You can't get the %s into the %s!" % (self, loc))
                loc.insert(self)  # put this object back into original Container
                return True
            cons.user.perceive('You pour the %s from the %s into the %s.' % (self, loc, oIDO))
            return True
        else:
            return "You can't pour the %s into the %s!" % (self, oIDO)
    
    def drink(self, p, cons, oDO, oIDO):
        if self != oDO: 
            return "Did you meant to drink the %s?" % self._short_desc
        self.emit("&nD%s drinks something." % cons.user.id, [cons.user])
        cons.user.perceive("You drink the %s." % self._short_desc)
        self.destroy()
        return True
    
