from debug import dbg
from thing import Thing
from action import Action

class Flashlight(Thing):
    def __init__(self, default_name, path):
        Thing.__init__(self, default_name, path)
        self.light = 0
        self.actions.append(Action(self.activate, ["activate", "turn"], True, True))
        self.actions.append(Action(self.put_away, ["hide"], True, True))
    
    def _adjust_descriptions(self):
        if self.light: 
            self.short_desc += " burning brightly"
            self.long_desc += "\nThe flashlight is on, burning brightly."
        else: 
            (head, sep, tail) = self.short_desc.partition(" burning brightly")
            self.short_desc = head
            (head, sep, tail) = self.long_desc.partition("\nThe flashlight is on")
            self.long_desc = head

    def put(self, p, cons, oDO, oIDO):
        (sV, sDO, sPrep, sIDO) = p.diagram_sentance(p.words)
        if sPrep == 'away' or sDO == 'away' or sIDO == 'away':      #TODO: Fix this up
            return self.put_away(p, cons, oDO, oIDO)
        else:
            return "I don't know what you mean by put in this context"
    
    def put_away(self, p, cons, oDO, oIDO):
        i = cons.user.visible_inventory.index(self)
        del cons.user.visible_inventory[i]
        if self.emits_light:
            self.change_room_light(self, -1)
        cons.write('You put away the flashlight')
        return True

    def activate(self, p, cons, oDO, oIDO):
        # TODO: emit something to the room when player turns flashlight on and off
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if sV == "activate": 
            if oDO != self:
                return "What are you trying to activate?"
            self.light = 1 if self.light == 0 else 0
            cons.write("You hit the switch on the flashlight, turning it %s." % 
                ("on" if self.light else "off"))
            self._adjust_descriptions()
            return True
        if sV == "turn":
            # could be "turn flashlight on", "turn off flashlight", etc
            if oDO == self and sIDO is not None: 
                return "I'm not sure what you mean."
            if (oDO == None and oIDO == self) or (oDO == self):
                if sPrep == "on":
                    if self.light == 0:
                        self.light = 1
                        cons.write("You turn on the flashlight.")
                    else: 
                        cons.write("The flashlight is already on!")
                elif sPrep == "off":
                    if self.light == 0:
                        cons.write("The flashlight is already off!")
                    else:
                        self.light = 0
                        cons.write("You turn off the flashlight.")
                else: # sPrep is some other preposition
                    return "I'm not sure what you mean."
                self._adjust_descriptions()
                return True
        return "I don't know what you mean by %s in this context." % sV
                
