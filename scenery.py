from debug import dbg
from thing import Thing
from action import Action

class Scenery(Thing):
    def __init__(self, ID, short_desc, long_desc, response_list=[]):
        """<response_list> is a list of tuples, each consisting of a 
        list of verbs and a result to be printed if the player uses one
        of the verbs on this object."""
        Thing.__init__(self, ID)
        self.fix_in_place("You can't move the %s!" % (ID))
        self.set_description(short_desc, long_desc)
        for item in response_list:
            self.actions.append(Action(self.handle_scenery_verb, item[0], True, False))
        self.responses = response_list
    
    def add_response(self, verbs, result):
        """If the player types one of the verbs in <verbs>, the game will print <result>"""
        self.responses.append((verbs, result))
        self.actions.append(Action(self.handle_scenery_verb, verbs, True, False))

    def handle_scenery_verb(self, p, cons, oDO, oIDO):
        verb = p.words[0]
        for i in self.responses:
            if verb in i[0]:
                cons.write(i[1])
                return
    