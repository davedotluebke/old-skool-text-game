from thing import Thing
from liquid import Liquid

from debug import dbg
from action import Action

class PinkPotion(Liquid):
    def drink(self, p, cons, oDO, oIDO):
        super().drink(p, cons, oDO, oIDO)
        cons.write('You drink the potion, and turn hot pink!')
        cons.user.emit('%s drinks the potion and turns bright pink!' % cons.user, ignore=[cons.user])
        return True

class InvisibilityPotion(Liquid):
    def drink(self, p, cons, oDO, oIDO):
        super().drink(p, cons, oDO, oIDO)
        cons.user.invisible = True      #TODO: Cleanup
        for i in Thing.ID_dict:
            if hasattr(i, 'game_redirect'):
                i.game_redirect.register_heartbeat(self)
                self.game_redirect = i.game_redirect
                break
        if hasattr(self, 'counters'):
            self.counters.append([cons.user, 10])
        else:
            self.counters = [[cons.user, 10]]
    
    def heartbeat(self):
        for i in self.counters:
            i[1] -= 1
            if i[1] <= 0:
                del self.counters[i]
                self.game_redirect.cons.user.invisible = False
