from room import Room
from player import Player
from thing import Thing

class TransportRoom(Room):
    def __init__(self, ID, transport_dest):
        super().__init__('spiraling confusion', pref_id=ID)
        self.set_description('spiraling confusion', "This is a confusing method of magical transport. You seem to be spinning through the air in a whirlwind. You're going so fast, however, that you can't quite make out anything you see along the way.")
        self.dest = transport_dest
        Thing.game.register_heartbeat(self)

    def heartbeat(self):
        for i in self.contents:
            i.move_to(self.dest)
            if isinstance(i, Player):
                i.cons.write(self.long_desc)
                i.cons.write("You find yourself falling to the ground.")
                i.cons.write("You land in a %s." % self.dest.short_desc)
                i.cons.write(self.dest.long_desc)
