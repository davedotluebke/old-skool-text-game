import random
import gametools

from thing import Thing
from liquid import Liquid
from room import Room

from debug import dbg
from action import Action

class PinkPotion(Liquid):
    def drink(self, p, cons, oDO, oIDO):
        if self != oDO: 
            return "Did you meant to drink the %s?" % self.short_desc
        cons.user.perceive('You drink the potion, and turn hot pink!')
        cons.user.emit('&nD%s drinks a potion and turns bright pink!' % cons.user, ignore=[cons.user])
        return True

class InvisibilityPotion(Liquid):
    def drink(self, p, cons, oDO, oIDO):
        if self != oDO: 
            return "Did you meant to drink the %s?" % self.short_desc
        cons.user.invisible = True      #TODO: Cleanup
        cons.game.events.schedule(cons.game.time+10, self.reappear, cons.user)
        self.emit('&nD%s drinks a potion and fades from sight.' % cons.user, [cons.user])
        cons.user.perceive('You drink the potion, and notice yourself fading away.')
        return True

    def reappear(self, user):
        user.invisible = False
        self.emit('&nI%s suddenly fades into sight, appearing as if out of thin air!' % user, [user])
        user.perceive('You notice you are now fading back into visibility.')
        
class StrengthPotion(Liquid):
    def drink(self, p, cons, oDO, oIDO):
        if self != oDO: 
            return "Did you meant to drink the %s?" % self.short_desc
        cons.user.perceive("You drink the potion, and feel stronger than you did before.")
        cons.user.emit('&nD%s drinks a potion. Nothing obvious happens...' % cons.user, ignore=[cons.user])
        cons.user.strength += 70
        cons.game.events.schedule(cons.game.time+15, self.wear_off, cons.user)
    
    def wear_off(self, user):
        user.strength -= 70
        cons.user.perceive("You feel like you could collapse in exhaustion now.")

class JumpingPotion(Liquid):
    def drink(self, p, cons, oDO, oIDO):
        if self != oDO:
            return "Did you mean to drink the %s?" % self.short_desc
        cons.user.perceive("You drink the potion, and fly up into the air!")
        cons.user.emit("&nD%s drinks a potion, and goes flying up into the air!")
        if hasattr(cons.user.location, 'jumping_destination'):
            cons.user.move_to(cons.user.location.jumping_destination)
            cons.user.perceive("You find yourself in a new place...")
            cons.user.location.report_arrival(cons.user)
            return True
        cons.user.perceive("You crash back down to the ground, gaining several bruises.")
        cons.user.emit("&nD%s crashes back down into the ground.")
        cons.user.health -= 2
        return True

class ExplorationPotion(Liquid):
    def drink(self, p, cons, oDO, oIDO):
        if self != oDO:
            return "Did you mean to drink the %s?" % self.short_desc
        cons.user.perceive("You drink the potion, and fly up into the air!")
        cons.user.emit("&nD%s drinks a potion, and goes flying up into the air!")
        all_python_files = gametools.findAllPythonFiles()
        dest = random.choice(all_python_files)
        try:
            gametools.load_room(gametools.findGamePath(dest)) #XXX needs to use full gamepath
        except Exception:
            return "This isn't working right now."
        return True
