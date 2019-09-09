from debug import dbg

from action import Action
from thing import Thing

class FaucetThing(Thing):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, ID, path, short_desc, long_desc, TYPE):
        super().__init__(ID, path)
        self.type = TYPE
        self.set_description(short_desc, long_desc)
        self.fix_in_place("You can't take the %s!" % self.type)
        self.add_names('faucet')
        self.running = 0
    
    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    # 
    def _adjust_descriptions(self):
        if self.running == 1:
            self._short_desc += ', with the water running'
            self._long_desc += ' The water in the %s is running.' % self.type
        if self.running == 0:
            (head, sep, tail) = self._short_desc.partition(", with the water running")
            self._short_desc = head
            (head, sep, tail) = self._long_desc.partition(" The water in the %s is running." % self.type)
            self._long_desc = head
        
    def toggle(self, p, cons, oDO, oIDO):
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if sV == "turn":
            # could be "turn water on", "turn off water", etc
            if oDO == self and sIDO is not None: 
                return "I'm not sure what you mean."
            if (oDO == None and (oIDO == self or sDO == 'water')) or (oDO == self or sIDO == 'water'):
                if sPrep == "on":
                    if self.running == 0:
                        self.running = 1
                        cons.write("You turn on the water.")
                    else: 
                        cons.write("The water is already on!")
                elif sPrep == "off":
                    if self.running == 0:
                        cons.write("The water is already off!")
                    else:
                        self.running = 0
                        cons.write("You turn off the water.")
                else: # sPrep is some other preposition
                    return "I'm not sure what you mean."
                self._adjust_descriptions()
                return True
        return "I don't know what you mean by %s in this context." % sV
    
    def fill_container(self, p, cons, oDO, oIDO):
        if oDO == None: 
            return "What do you intend to fill from the %s?" % self.type
        
        filling = oDO
        if not getattr(filling, 'liquid'):
            cons.write('The water leaves the %s and goes down the drain in the %s.' % (filling, self.type))
            return True
        cons.write('Water comes out of the faucet and fills your %s.' % filling)
        self.emit('&nD%s fills a %s with water at the %s.' % (cons.user.id, filling, self.type))
        water = gametools.clone('domains.school.school.water')
        oDO.insert(water)
        return True
    
    def pour_out_in_self(self, p, cons, oDO, oIDO):
        if oDO:
            obj = oDO
        else:
            obj = oIDO
        if obj == self or obj == None:
            return "Imposible to pour out a %s in a %s." % (self.type, self.type)
        cons.write('You pour the %s into the %s, and it goes down the drain.' % (obj, self.type))
        self.emit('&nD%s pours the %s into the %s, and it goes down the drain.' % (cons.user.id, obj, self.type))
        obj.move_to(Thing.ID_dict['nulspace'])
        return True

    actions = dict(Thing.actions)  # make a copy
    actions['fill'] = Action(fill_container, True, False)
    actions['pour'] = Action(pour_out_in_self, True, False)
    actions['turn'] = Action(toggle, True, True)
