from debug import dbg
from action import Action

from thing import Thing

class Flower(Thing):
    def __init__(self, default_name, type=None):
        super().__init__(default_name)
        self.type = type
        self.actions.append(Action(self.pick, ['pick', 'take', 'pluck'], True, False))
        self.actions.append(Action(self.shake, ['shake'], True, False, ['held']))

    def pick(self, p, cons, oDO, oIDO):
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if oDO == self:
            if not oIDO:
                return self.take(p, cons, oDO, oIDO)
            else:
                return 'I\'m not sure what you mean.'
        if oIDO == self:
            if sDO == 'petal' and sPrep in ['from', 'off']:
                petal = Thing(self.names[0] + ' petal')
                petal.set_description(self.names[0] + ' petal', "This is a single petal from a %s" % self.names[0])
                petal.add_names('petal')
                petal.add_adjectives(self.names[0])
                petal.set_volume(0.0005)
                petal.set_weight(0.5)
                petal.move_to(cons.user)
                return True
            else:
                return "I'm not sure what you are trying to pick from the %s...a petal perhaps?" % self.names[0]
        return "I'm not sure what you mean! "
    
    def shake(self, p, cons, oDO, oIDO):
        for i in self.actions:
            if i.func == self.shake:
                if not i.validate:
                    cons.write("You have to pick the flower before you can shake it!")
                    return True
        if self.type in ['poppy']:
            cons.write('You shake the flower, and collect some %s seeds.' % self.names[0])
            seed = Thing('%sseed' % self.names[0])
            seed.set_description(seed.names[0], 'This is a normal %s seed.' % self.names[0])
            seed.move_to(cons.user)
            return True
        else:
            cons.write('You shake the flower, and nothing happens.')
            return True
