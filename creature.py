import random
from debug import dbg

from container import Container

class Creature(Container):
        def __init__(self, ID):
                Container.__init__(self, ID)
                self.hitpoints = 10           # default hitpoints
                self.health = self.hitpoints  # default full health (0 health --> dead)

class NPC(Creature):
        def __init__(self, ID, g):
                Creature.__init__(self, ID)
                self.aggressive = False
                self.move_soon = 0
                self.move_frequency = 3
                g.register_heartbeat(self)
        
        def heartbeat(self):
                self.move_soon += 1
                dbg.debug('beat')
                if self.move_soon == self.move_frequency:
                        self.move_soon = 0
                        dbg.debug("Moving")
                        self.move_around()

        def move_around(self):
                exit = random.choice(list(self.location.exits))
                dbg.debug("Trying to move to the %s exit!" % (exit))
                current_room = self.location
                new_room = self.location.exits[exit]
                current_room.extract(self)
                new_room.insert(self)
                dbg.debug("Moved to new room %s" % (new_room.id))