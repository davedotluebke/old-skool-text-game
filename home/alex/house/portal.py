# this file does not contain completely working code, and should not be used
'''import gametools
import thing
import debug

class DebugPortal(thing.Thing):
    def __init__(self, default_name, path):
        super().__init__(default_name, path)
        self.set_description('vortex', 'This object looks like it contains a vortex. Otherwise, it is smooth and shiney.')
        self.add_names('portal', 'vortex')
        self.actions.append(thing.Action(self.open, ['open'], True, False))
        self.cons = None
        self.dbg = thing.Thing.game.dbg
        self.room = None

    def open(self, p, cons, oDO, oIDO):
        if self.cons:
            return "Attempts to open the portal are failing."
        
        cons.user.perceive('You open the portal, and see a shimmering shaft of light, followed by text.')
        cons.user.emit('&nD%s somehow opens the vortex.' % cons.user)
        cons.request_input(self)
        self.cons = cons
        

        return True

    def console_recv(self, user_input):
        if user_input == 'quit':
            self.cons.write('You feel like you emerge from the vortex.')
            self.room = None
            self.cons.input_redirect = None
            self.cons
            return
        self.room = gametools.load_room(user_input)
        if self.room == None:
            self.cons.write('Please enter a valid room path.')
            return
        self.room.insert(cons.user)

def clone():
    return DebugPortal('portal', __file__)'''
