import liquid
import gametools
import thing
import room

class LiquidFire(liquid.Liquid):
    def pour(self, p, cons, oDO, oIDO):
        c = self.location
        cauldron = (self.location.path == 'domains.school.elementQuest.cauldron')
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
        while loc.location:
            if loc.path == 'domians.school.elementQuest':
                break
            if isinstance(loc, room.Room):
                break
            loc = loc.location
        if not loc.indoor:
            self.burn_up()
    
    def burn_up(self)
        self.emit('The luminous red liquid in the %s bursts into flames and quickly burns away.' % self.location)
        self.move_to(thing.Thing.ID_dict['nulspace'])

def clone():
    f = LiquidFire('liquid', 'luminous red liquid', 'This luminous red liquid shimmers, almost as if it were in flames.')
    f.path = 'domains.school.elementQuest.liquid_fire'
    f.add_adjectives('luminous', 'red')
    thing.Thing.game.register_heartbeat(f)
    return f
