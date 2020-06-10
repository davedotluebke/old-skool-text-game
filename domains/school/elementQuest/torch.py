import thing
import action

class Torch(thing.Thing):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self):
        super().__init__('torch', __file__)
        self.set_description('makeshift torch', 'This makeshift wooden torch is made of an oak branch with a cloth wrapped around the end.')
        self.add_adjectives('makeshift', 'wooden')
        self.add_names('branch', 'cloth')
        self.lit = False
        self.soaked = False
    
    #
    # OTHER EXTERNAL METHODS (misc externally visible methods)
    #
    def soak_torch(self):
        self.soaked = True
        self.set_description('makeshift torch soaked with a red liquid', 'This makeshift wooden torch is made of an oak branch with a cloth wrapped around the end and soaked with a red liquid.')

    def light_torch(self):
        self.lit = True
        self.set_description('makeshift torch, burning brightly', 'This wooden torch is made of an oak branch with a cloth wrapped around the end. It is burning brightly.')
    
    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    #
    def hold(self, p, cons, oDO, oIDO):
        u = cons.user
        verb = p.words[0]
        if oIDO == None:
            if self.location == u and oDO == self:
                return "You are already holding the torch!"
            return "I'm not quite sure what you meant."
        if oIDO.names[0] == 'shaft':
            if self.lit: 
                cons.write('You %s the burning torch in the shaft of sunlight, but nothing '
                            'further happens.' % verb)
                self.emit("&nD%s %ss the burning torch in the shaft of sunlight." % (u.id, verb),
                            [u])
                return True
            if self.soaked:
                cons.write('The luminous red liquid in the cloth bursts into flame and starts the torch burning brightly.')
                self.emit('&nD%s %ss the torch in the shaft of sunlight, and it suddenly bursts into flames!' % (u.id, verb), [u])
                self.light_torch()
                return True
            else:  # unlit torch is not soaked
                cons.write('You %s the torch in the shaft of sunlight, but nothing happens.' % verb)
                self.emit("&nD%s %ss the torch in the shaft of sunlight." % (u.id, verb), [u])
                return True
                
        if oIDO.names[0] == 'door':
            if self.lit:
                cons.write('You %s the torch to the door, setting it aflame.' % verb)
                self.location.emit('&nD%s %ss the torch to the door, quickly setting it aflame.' % (u.id, verb))
                oIDO.burn(self)
                return True
        return "I'm not quite sure what you meant."
        
    actions = dict(Thing.actions)  # make a copy
    actions['hold'] = Action(hold, True, False) 
    actions['wave'] = Action(hold, True, False) 
    actions['thrust'] = Action(hold, True, False) 

#
# MODULE-LEVEL FUNCTIONS (e.g., clone() or load())
#
def clone():
    return Torch()