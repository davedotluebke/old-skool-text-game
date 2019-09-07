from debug import dbg
from action import Action

from thing import Thing
import gametools

class Flower(Thing):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, default_name, path, type=None, pref_id=None):
        super().__init__(default_name, path)
        self.type = type

    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    # 
    def pick(self, p, cons, oDO, oIDO):
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if oDO == self:
            if not oIDO:
                return self.take(p, cons, oDO, oIDO)
            else:
                return 'I\'m not sure what you mean.'
        if oIDO == self:
            if sDO == 'petal' and sPrep in ['from', 'off']:
                import domains.school.forest.petal as petal_path
                petal_path.set_species(self.type)
                petal = gametools.clone("domains.school.forest.petal")
                petal.move_to(cons.user)
                cons.write('You pick a petal from the %s.' % self.type)
                cons.user.emit("&nD%s picks a petal from a %s.", (cons.user.id, self.type))
                return True
            else:
                return "I'm not sure what you are trying to pick from the %s...a petal perhaps?" % self.names[0]
        return "I'm not sure what you mean! Are you trying to pick the %s or pick something from the %s? " % (self.names[0], self.names[0])
    
    def shake(self, p, cons, oDO, oIDO):
        if self not in cons.user.contents:
            cons.write("You have to pick the flower before you can shake it!")
            return True
        if self.type in ['poppy']:
            cons.write('You shake the flower and collect some %s seeds.' % self.names[0])
            cons.user.emit("&nD%s shakes a flower and collects some seeds." % cons.user.id)
            seed = gametools.clone('domains.school.forest.seed')
            seed.move_to(cons.user)
            return True
        else:
            cons.write('You shake the flower, and nothing happens.')
            return True

    actions = dict(Thing.actions)
    actions['pick'] =   Action(pick, True, False)
    actions['take'] =   Action(pick, True, False)
    actions['pluck'] =  Action(pick, True, False)
    actions['shake'] =  Action(shake, True, False)
    