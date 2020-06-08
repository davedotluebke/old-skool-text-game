from thing import Thing
from action import Action
import gametools

class Scenery(Thing):
    def __init__(self, default_name, short_desc, long_desc, pref_id=None, unlisted=False):
        Thing.__init__(self, default_name, None)
        self.fix_in_place("You can't move the %s!" % (default_name))
        self.set_description(short_desc, long_desc)
        self.unlisted = unlisted
        self.versions[gametools.findGamePath(__file__)] = 1

        self.actions = dict(Thing.actions)
        # response tuple is (verblist, result_str, transitive, intransitive)
        self.responses = []     # list of response tuples
    
    def add_response(self, verbs, result, trans=True, intrans=False, emit_message=None):
        """Specify a list of <verbs> that, when used, will print <result>. 
        
        Set <trans> flag for transitive verbs to be used on this object.
        Set <intrans> flag for intransitive verbs that can be used alone."""
        
        self.responses.append((verbs, result, trans, intrans, emit_message))
        for v in verbs:
            self.actions[v] = Action(Scenery.handle_verb, trans, intrans)
        
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
        