import thing

class Torch(thing.Thing):
    def __init__(self):
        super().__init__('torch', __file__)
        self.set_description('makeshift torch', 'This wooden torch is made of an oak branch with a cloth wrapped around the end.')
        self.add_adjectives('makeshift', 'wooden')
        self.add_names('branch', 'cloth')
        self.lit = False
        self.soaked = False
    
    def light(self):
        self.lit = True
        self.set_description('makeshift torch, burning brightly', 'This wooden torch is made of an oak branch with a cloth wrapped around the end. It is burning brightly.')

    def hold(self, p, cons, oDO, oIDO):
        if oIDO.names[0] == 'shaft':
            if self.soaked and not self.lit:
                cons.write('The liquid fire in the cloth bursts into flame, and starts the torch burning brightly.')
                self.emit('%s holds the torch in the shaft of sunlight and it suddenly bursts into flames!' % cons.user, [cons.user])
                self.light()
                return True
        if oIDO.names[0] == 'door':
            pass
        if oIDO.names[0] == 'firepit':
            pass

def clone():
    return Torch()