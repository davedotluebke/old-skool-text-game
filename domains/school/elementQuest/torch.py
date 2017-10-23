import thing
import action

class Torch(thing.Thing):
    def __init__(self):
        super().__init__('torch', __file__)
        self.set_description('makeshift torch', 'This makeshift wooden torch is made of an oak branch with a cloth wrapped around the end.')
        self.add_adjectives('makeshift', 'wooden')
        self.add_names('branch', 'cloth')
        self.actions.append(action.Action(self.hold, ['hold', 'wave', 'thrust'], True, False))
        self.lit = False
        self.soaked = False
    
    def soak_torch(self):
        self.soaked = True
        self.set_description('makeshift torch, soaked with a red liquid', 'This makeshift wooden torch is made of an oak branch, with a cloth wrapped around the end and soaked with a red liquid.')

    def light_torch(self):
        self.lit = True
        self.set_description('makeshift torch, burning brightly', 'This wooden torch is made of an oak branch with a cloth wrapped around the end. It is burning brightly.')

    def hold(self, p, cons, oDO, oIDO):
        if oIDO == None:
            if self.location == cons.user and oDO == self:
                return "You are already holding the torch!"
            return "I'm not quite sure what you meant."
        if oIDO.names[0] == 'shaft':
            if self.lit: 
                cons.write('You %s the burning torch in the shaft of sunlight, but nothing '
                            'further happens.' % p.words[0])
                self.emit("%s %ss the burning torch in the shaft of sunlight." % (cons.user, p.words[0]), 
                            [cons.user])
                return True
            if self.soaked:
                cons.write('The luminous red liquid in the cloth bursts into flame, and starts the torch burning brightly.')
                self.emit('%s holds the torch in the shaft of sunlight and it suddenly bursts into flames!' % cons.user, [cons.user])
                self.light_torch()
                return True
            else:  # unlit torch is not soaked
                cons.write('You %s the torch in the shaft of sunlight, but nothing happens.' % p.words[0])
                self.emit("%s %ss the torch in the shaft of sunlight." % (cons.user, p.words[0]), [cons.user])
                return True
                
        if oIDO.names[0] == 'door':
            if self.lit:
                cons.write('You hold the torch on the door, setting it into flames.')
                oIDO.burn(self)
                return True
        return "I'm not quite sure what you meant."

def clone():
    return Torch()