import scenery
import gametools
import thing
import action

class Keyhole(scenery.Scenery):
    def __init__(self, exit_direction, exit_dest, qkey_number):
        super().__init__('keyhole', 'keyhole embeded in the rock face', 'This keyhole is embeded in the rock face. You cannot see any other sign of a door.')
        self.unlisted = True
        self.actions['put'] = action.Action(Keyhole.open_door, True, False)
        self.actions['insert'] = action.Action(Keyhole.open_door, True, False)
        self.checked_players = []
        self.exit_direction = exit_direction
        self.exit_dest = exit_dest
        self.numq = qkey_number
    
    def open_door(self, p, cons, oDO, oIDO):
        if hasattr(oDO, 'qkey_number') and oDO.qkey_number == self.numq:
            cons.user.perceive('As soon as you insert the key, the massive rock wall begins to part, revealing a passage to the %s.' % self.exit_direction)
            self.location.add_exit(self.exit_direction, self.exit_dest)
            oDO.move_to(thing.Thing.ID_dict['nulspace'])
            self.checked_players.append(cons.user)
            return True
        else:
            cons.user.perceive("You try to put the %s in the keyhole, but it doesn't fit." % oDO.names[0])
            return True
          