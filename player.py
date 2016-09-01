from creature import Creature

class Player(Creature):
    def __init__(self,ID):
        Creature.__init__(self, ID)
        self.new_verb("inventory", self.inventory)

    def inventory(self, cons, oDO, oIDO):
        cons.write("You are carrying:")
        for i in self.contents:
            cons.write(i.id)