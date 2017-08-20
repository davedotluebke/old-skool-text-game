from thing import Thing
from debug import dbg
from action import Action

from scenery import Scenery
from container import Container

class Liquid(Scenery):
    def __init__(self, default_name, short_desc = None, long_desc = None, pref_id=None):
        Scenery.__init__(self, default_name, short_desc, long_desc, pref_id)
        self.actions.append(Action(self.pour, ['pour'], True))
        self.actions.append(Action(self.drink, ['drink', 'sip', 'taste'], True))
        self.is_liquid = True

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
                self.move_to(Thing.ID_dict['nulspace'])
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
            return "Did you meant to drink the %s?" % self.short_desc
        self.emit("%s drinks something." % cons.user, [cons.user])
        cons.user.perceive("You drink the %s." % self.short_desc)
        self.move_to(Thing.ID_dict['nulspace'])
        return True
    
    


