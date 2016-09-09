from creature import Creature

class Player(Creature):
    def __init__(self,ID, console):
        """Initialize the Player object and attach a console"""
        Creature.__init__(self, ID)
        self.cons = console
        self.new_verb("inventory", self.inventory)
        self.set_weight(175/2.2)
        self.set_volume(66)

    def perceive(self, message):
        Creature.perceive(self, message)
        self.cons.write(message)        

    def inventory(self, cons, oDO, oIDO):
        cons.write("You are carrying:")
        for i in self.contents:
            cons.write(i.id)