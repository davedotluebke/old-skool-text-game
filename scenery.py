from debug import dbg
from thing import Thing
from action import Action

class Scenery(Thing):
    def __init__(self, ID, short_desc, long_desc,):
        Thing.__init__(self, ID)
        self.fix_in_place("You can't move the %s!" % (ID))
        self.set_description(short_desc, long_desc)
        # response tuple is (verblist, result_str, transitive, intransitive)
        self.responses = []     # list of response tuples
    
    def add_response(self, verbs, result, trans=True, intrans=False, emit_message=None):
        """Specify a list of <verbs> that, when used, will print <result>. 
        
        Set <trans> flag for transitive verbs to be used on this object.
        Set <intrans> flag for intransitive verbs that can be used alone."""
        
        self.responses.append((verbs, result, trans, intrans, emit_message))
        self.actions.append(Action(self.handle_verb, verbs, trans, intrans))
        
    def handle_verb(self, p, cons, oDO, oIDO):
        verb = p.words[0]
        for response in self.responses:
            verbs, result, transitive, intransitive, emit_message = response
            if verb in verbs:        
                if (intransitive and not oDO) or (transitive and oDO == self):
                    cons.write(result)
                    if emit_message:
                        cons.user.emit(emit_message % (cons.user), ignore=[cons.user])
                    return True
        return "I'm not sure what you mean by " + verb + " in this context."
        