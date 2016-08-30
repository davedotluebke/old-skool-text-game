from creature import *

class Player(Creature):
    def __init__(self,ID):
        Creature.__init__(self, ID)
        self.cons = None
        self.new_verb("inventory", self.inventory)

    def connect_console(self, c):
        self.cons = c
    def inventory(self, cons, oDO, oIDO):
        cons.write("You are carrying:")
        for i in self.contents:
            cons.write(i.id)