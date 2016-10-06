from creature import Creature
from action import Action

class Player(Creature):
    def __init__(self,ID, console):
        """Initialize the Player object and attach a console"""
        Creature.__init__(self, ID)
        self.cons = console
        self.set_weight(175/2.2)
        self.set_volume(66)
        self.new_verb("inventory", self.inventory)
        inv = Action(self.inventory, "inventory", False, True)
        self.actions.append(inv)

    def perceive(self, message):
        Creature.perceive(self, message)
        self.cons.write(message)        

    def inventory(self, p, cons, oDO, oIDO):
        cons.write("You are carrying:")
        if not self.contents:
            cons.write('nothing')
        for i in self.contents:
            cons.write(i.id)