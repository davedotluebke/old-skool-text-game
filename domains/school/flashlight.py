from thing import Thing
from action import Action
import gametools 

class Flashlight(Thing):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, default_name, path):
        Thing.__init__(self, default_name, path)
        self.log.info("Created flashlight with id %s" % self.id)
        self.light = 0
    
    #
    # INTERNAL USE METHODS (i.e. _method(), not imported)
    #
    def _adjust_descriptions(self):
        if self.light: 
            self._short_desc += " burning brightly"
            self._plural_short_desc += " burning brightly"
            self._long_desc += "\nThe flashlight is on, burning brightly."
            self.add_adjectives("lit", "burning")
        else: 
            (head, sep, tail) = self._short_desc.partition(" burning brightly")
            self._short_desc = head
            (head, sep, tail) = self._plural_short_desc.partition(" burning brightly")
            self._plural_short_desc = head
            (head, sep, tail) = self._long_desc.partition("\nThe flashlight is on")
            self._long_desc = head
            self.remove_adjectives("lit", "burning")
        self.log.debug("Flashlight description adjusted; new description '%s'" % self._long_desc)

    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    # 
    def put(self, p, cons, oDO, oIDO):
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if sPrep == 'away' or sDO == 'away' or sIDO == 'away':      #TODO: Fix this up
            return self.put_away(p, cons, oDO, oIDO)
        else:
            self.log.warning("User said 'put' but not 'put away'")
            return "I don't know what you mean by put in this context"
    
    def put_away(self, p, cons, oDO, oIDO):
        if self.emits_light:
            self.change_room_light(self, -1)
        cons.user.perceive('You put away the flashlight')
        return True

    def activate(self, p, cons, oDO, oIDO):
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if sV == "activate": 
            if oDO != self:
                return "What are you trying to activate?"
            self.light = 1 if self.light == 0 else 0
            cons.user.perceive("You hit the switch on the flashlight, turning it %s." % ("on" if self.light else "off"))
            self.emit("&nD%s turns %s a flashlight." % (cons.user.id, "on" if self.light else "off"))
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
                        cons.user.perceive("You turn on the flashlight.")
                        self.emit("&nD%s turns on a flashlight." % cons.user.id)
                    else: 
                        cons.user.perceive("The flashlight is already on!")
                elif sPrep == "off":
                    if self.light == 0:
                        cons.user.perceive("The flashlight is already off!")
                    else:
                        self.light = 0
                        cons.user.perceive("You turn off the flashlight.")
                        self.emit("&nD%s turns off the flashlight." % cons.user.id)
                else: # sPrep is some other preposition
                    return "I'm not sure what you mean."
                self._adjust_descriptions()
                return True
        return "I don't know what you mean by %s in this context." % sV

    actions = dict(Thing.actions)
    actions['activate'] = Action(activate, True, True)
    actions['turn']     = Action(activate, True, False)
    actions['hide']     = Action(put_away, True, True)
    actions['put']      = Action(put, True, False)

#
# MODULE-LEVEL FUNCTIONS (e.g., clone() or load())
#

def clone():
    flashlight = Flashlight('flashlight', __file__)
    flashlight.set_description('old flashlight', 'An old metal flashlight.')
    return flashlight
