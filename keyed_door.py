import doors_and_windows
import action
import gametools

class KeyedDoor(doors_and_windows.Door):
    def __init__(self, default_name, short_desc, long_desc, dest, direction, matching_key):
        super().__init__(default_name, short_desc, long_desc, dest, direction)
        self.matching_key = matching_key
        self.actions['lock'] = action.Action(KeyedDoor.lock_door, True, False)
        self.actions['unlock'] = action.Action(KeyedDoor.unlock_door, True, False)

    def lock_door(self, p, cons, oDO, oIDO):
        if self.locked:
            return "The door is already locked!"
        if self.open_state:
            value = self.close_door(p, cons, oDO, oIDO)
            if value != True:
                return value
        if not oIDO or oIDO.path != self.matching_key:
            cons.user.perceive("You don't have the key.")
            return True

        self.locked = True
        self.toggle_matching(True, self.open_state)
        cons.user.perceive('You lock the door.')
        cons.user.emit('&nD%s locks the door.')
        return True

    def unlock_door(self, p, cons, oDO, oIDO):
        if not self.locked:
            return "The door is already unlocked!"
        if not oIDO or oIDO.path != self.matching_key:
            cons.user.perceive("You don't have the key.")
            return True
        self.locked = False
        self.toggle_matching(False, self.open_state)
        cons.user.perceive('You unlock the door.')
        cons.user.emit('&nD%s unlocks the door.')
        return True
