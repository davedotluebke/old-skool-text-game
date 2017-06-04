from thing import Thing
from liquid import Liquid

from debug import dbg
from action import Action

class PinkPotion(Liquid):
    def drink(self, p, cons, oDO, oIDO):
        if self != oDO: 
            return "Did you meant to drink the %s?" % self.short_desc
        cons.user.perceive('You drink the potion, and turn hot pink!')
        cons.user.emit('%s drinks the potion and turns bright pink!' % cons.user, ignore=[cons.user])
        return True

class InvisibilityPotion(Liquid):
    def drink(self, p, cons, oDO, oIDO):
        if self != oDO: 
            return "Did you meant to drink the %s?" % self.short_desc
        cons.user.invisible = True      #TODO: Cleanup
        cons.game.events.schedule(cons.game.time+10, self.reappear, cons.user)
        self.emit('%s drinks a potion and fades from sight.' % cons.user, [cons.user])
        cons.user.perceive('You drink the potion, and notice yourself fading away.')
        return True

    def reappear(self, user):
        user.invisible = False
        self.emit('%s suddenly fades into sight, appearing as if out of thin air!' % user, [user])
        user.perceive('You notice you are now fading back into visibility.')
        
       
