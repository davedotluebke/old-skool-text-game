from liquid import Liquid

from debug import dbg
from action import Action

class PinkPotion(Liquid):
    def drink(self, p, cons, oDO, oIDO):
        super().drink(p, cons, oDO, oIDO)
        cons.write('You drink the potion, and turn hot pink!')
        cons.user.emit('%s drinks the potion and turns bright pink!' % cons.user, ignore=cons.user)
        return True

class InvisibilityPotion(Liquid):
    def drink(self, p, cons, oDO, oIDO):
        super().drink(p, cons, oDO, oIDO)
        cons.user.invisible = True      #TODO: Wares of after certain # of turns
