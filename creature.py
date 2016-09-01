from container import Container

class Creature(Container):
        def __init__(self, ID):
                Container.__init__(self, ID)
                self.hitpoints = 10           # default hitpoints
                self.health = self.hitpoints  # default full health (0 health --> dead)
