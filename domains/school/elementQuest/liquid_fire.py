import liquid
import gametools
import thing

class LiquidFire(liquid.Liquid):
    def pour(self, p, cons, oDO, oIDO):
        c = self.location
        cauldron = (self.location.path == 'domains.school.elementQuest.cauldron')
        v = super().pour(p, cons, oDO, oIDO)
        if self not in c.contents:
            c.insert(gametools.clone(self.path)) # refill the cauldron
        return v


