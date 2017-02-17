from debug import dbg
from thing import Thing
from action import Action

class Flashlight(Thing):
    def __init__(self, default_name):
        Thing.__init__(self, default_name)
        self.emits_light = 0
        self.actions.append(Action(self.activate, ["activate", "turn"], True, True))
        self.actions.append(Action(self.use, ["use"], True, False))
        self.actions.append(Action(self.put_away, ["hide"], True, True))
    
    def _adjust_descriptions(self):
        if self.emits_light: 
            self.short_desc += " burning brightly"
            self.long_desc += "\nThe flashlight is on, burning brightly."
        else: 
            (head, sep, tail) = self.short_desc.partition(" burning brightly")
            self.short_desc = head
            (head, sep, tail) = self.long_desc.partition("\nThe flashlight is on")
            self.long_desc = head

    def change_room_light(self, delta):
        """Change light level in the containing room by delta. Call only when emit_light changes."""
        loc = self.location
        while loc:
            if hasattr(loc, "light"):
                # loc is a Room, increase it's light level
                loc.light += delta
                break
            if loc.see_inside or (hasattr(loc, 'cons') and (self in loc.visible_inventory)):
                # loc is a Container that passes light, recurse or loc is a Player using the flashlight, recurse
                loc = loc.location
            else:
                break

    def use(self, p, cons, oDO, oIDO):
        if self.location == cons.user:
            cons.user.visible_inventory.append(self)
            if self.emits_light:
                self.change_room_light(1)
            cons.write('You shine the flashlight around the %s.' % cons.user.location)
            return True
        elif self.location == cons.user.location:
            self.move_to(cons.user)
            cons.user.visible_inventory.append(self)
            cons.write('You take the flashlight and shine it around the %s.' % cons.user.location)
            if self.emits_light:
                self.change_room_light(1)
            return True
        else:
            return "I'm not quite sure what you are trying to do in this case."

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
            if self.emits_light: 
                self.emits_light = 0
                self.change_room_light(-1)
            else:
                self.emits_light = 1
                self.change_room_light(1)
            cons.write("You hit the switch on the flashlight, turning it %s." % 
                ("on" if self.emits_light else "off"))
            self._adjust_descriptions()
            return True
        if sV == "turn":
            # could be "turn flashlight on", "turn off flashlight", etc
            if oDO == self and sIDO is not None: 
                return "I'm not sure what you mean."
            if (oDO == None and oIDO == self) or (oDO == self):
                if sPrep == "on":
                    if self.emits_light == 0:
                        self.emits_light = 1
                        self.change_room_light(1)
                        cons.write("You turn on the flashlight.")
                    else: 
                        cons.write("The flashlight is already on!")
                elif sPrep == "off":
                    if self.emits_light == 0:
                        cons.write("The flashlight is already off!")
                    else:
                        self.emits_light = 0
                        self.change_room_light(-1)
                        cons.write("You turn off the flashlight.")
                else: # sPrep is some other preposition
                    return "I'm not sure what you mean."
                self._adjust_descriptions()
                return True
        return "I don't know what you mean by %s in this context." % sV
                
