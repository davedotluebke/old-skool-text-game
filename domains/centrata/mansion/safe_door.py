import doors_and_windows
import action

class SafeDoorOutside(doors_and_windows.Door):
    def __init__(self):
        super().__init__('door', 'safe door', 'This is a very heavy door designed to keep people out of a safe.', 'domains.centrata.mansion.safe', 'west')
        self.add_adjectives('safe', 'heavy', 'very')
        self.locked = True
        self.code = "9124" # this is intentionally a string, because it is intended to be compared to user input

        self.actions['lock'] = action.Action(SafeDoorOutside.lock_door, True, False)
        self.actions['unlock'] = action.Action(SafeDoorOutside.unlock_door, True, False)

    def lock_door(self, p, cons, oDO, oIDO):
        if self.locked:
            return "The door is already locked!"
        if self.open_state:
            value = self.close_door(p, cons, oDO, oIDO)
            if value != True:
                return value
        
        sV, sDO, sPrep, sIDO = p.diagram_sentence(p.words)
        if not sIDO or not sIDO.isdigit():
            cons.user.perceive("The dial only displays the numbers 0-9.")
            return True
        
        if sIDO != self.code:
            cons.user.perceive("The code is incorrect.")
            return True

        self.locked = True
        self.toggle_matching(True, self.open_state)
        cons.user.perceive('You lock the door.')
        cons.user.emit('&nD%s locks the door.')
        return True
    
    def unlock_door(self, p, cons, oDO, oIDO):
        if not self.locked:
            return "The door is already unlocked!"
        
        sV, sDO, sPrep, sIDO = p.diagram_sentence(p.words)
        if not sIDO or not sIDO.isdigit():
            cons.user.perceive("The dial only displays the numbers 0-9.")
            return True
        
        if sIDO != self.code:
            cons.user.perceive("The code is incorrect.")
            return True
        
        self.locked = False
        self.toggle_matching(False, self.open_state)
        cons.user.perceive('You unlock the door.')
        cons.user.emit('&nD%s unlocks the door.')
        return True

class SafeDoorInside(doors_and_windows.Door):
    def __init__(self):
        super().__init__('door', 'safe door', 'This is a very heavy door designed to keep people out of a safe.', 'domains.centrata.mansion.office', 'east')
        self.add_adjectives('safe', 'heavy', 'very')
        self.locked = True
        self.code = "9124" # this is intentionally a string, because it is intended to be compared to user input

        self.actions['lock'] = action.Action(SafeDoorInside.lock_door, True, False)
        self.actions['unlock'] = action.Action(SafeDoorInside.unlock_door, True, False)

    def lock_door(self, p, cons, oDO, oIDO):
        if self.locked:
            return "The door is already locked!"
        if self.open_state:
            value = self.close_door(p, cons, oDO, oIDO)
            if value != True:
                return value
        
        sV, sDO, sPrep, sIDO = p.diagram_sentence(p.words)
        if not sIDO or not sIDO.isdigit():
            cons.user.perceive("The dial only displays the numbers 0-9.")
            return True
        
        if sIDO != self.code:
            cons.user.perceive("The code is incorrect.")
            return True

        self.locked = True
        self.toggle_matching(True, self.open_state)
        cons.user.perceive('You lock the door.')
        cons.user.emit('&nD%s locks the door.')
        return True
    
    def unlock_door(self, p, cons, oDO, oIDO):
        if not self.locked:
            return "The door is already unlocked!"
        
        # unlocking is always possible from within
        
        self.locked = False
        self.toggle_matching(False, self.open_state)
        cons.user.perceive('You unlock the door.')
        cons.user.emit('&nD%s unlocks the door.')
        return True
