import liquid
import gametools
from thing import Thing
import room

class LiquidFire(liquid.Liquid):
    def pour(self, p, cons, oDO, oIDO):
        c = self.location
        cauldron = (self.location.path == 'domains.school.elementQuest.cauldron')
        if oIDO == None: 
            return 'What do you want to pour into (or onto) what?'
        if hasattr(oIDO, 'soaked'):
            oIDO.soak_torch()
            cons.user.perceive('You soak the %s with the red liquid.' % oIDO)
            oIDO.emit('&nD%s pours a red liquid over the %s, soaking it thoroughly.' % (cons.user.id, oIDO), [cons.user])
            self.move_to(Thing.ID_dict['nulspace'])
            return True
        if oIDO.contents == None:
            cons.user.perceive('You pour the red liquid over the %s, but it quickly drips off and soaks into the ground.' % oIDO)
            oIDO.emit('&nD%s pours a red liquid over a %s. It quickly drips off and disappears into the ground.' % (cons.user.id, oIDO), [cons.user])
            return True
        for i in oIDO.contents:
            if i.path == self.path:
                cons.write("You pour some more of the liquid into the %s." % oIDO)
                return True
        v = super().pour(p, cons, oDO, oIDO)
        if self not in c.contents and cauldron:
            c.insert(gametools.clone(self.path)) # refill the cauldron
        return v

    def heartbeat(self):
        loc = self.location
        if loc == str(loc):
            return
        while loc.location:
            if loc.path == 'domains.school.elementQuest':
                break
            if isinstance(loc, room.Room):
                break
            loc = loc.location
        if not loc.indoor:
            self.burn_up()
    
    def burn_up(self):
        self.emit('The luminous red liquid in the %s bursts into flames and quickly burns away.' % self.location)
        self.move_to(Thing.ID_dict['nulspace'])

def clone():
    f = LiquidFire('liquid', 'luminous red liquid', 'This luminous red liquid shimmers, almost as if it were in flames.')
    f.path = 'domains.school.elementQuest.liquid_fire'
    f.add_adjectives('luminous', 'red')
    Thing.game.register_heartbeat(f)
    return f
