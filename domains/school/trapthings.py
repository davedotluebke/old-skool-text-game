from thing import Thing
from room import Room

class TrapThing(Thing):
    def __init__(self, default_name, trap_message, trap_location, ID):
        super().__init__(default_name, ID)
        self.trap_message = trap_message
        self.trap_location = trap_location
    
    def take(self, p, cons, oDO, oIDO):
        if oDO != self and oIDO != self:
            return "I don't understand what your'e trying to take!"
        cons.write(self.trap_message)
        cons.user.move_to(self.trap_location)
        return True
