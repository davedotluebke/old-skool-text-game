from debug import dbg

class Action:
    """An action the player can do, associated with an object in the game.
    Specifies a function <func> which is enacted by the player using one or more 
    verb synonums (strings in <verblist>).  Verbs can be <transitive> (taking a 
    direct object), <intransitive> (no direct object), or both.
    
    Action functions take the special form 
        a(parser, console, DO, IDO)
    where parser and console are from the current client, DO is the object 
    that the parser has determined is the direct object of the user's command
    (or None if the verb is intransitive), IDO is the indirect object (if any). 
    Action functions return True if the usage was valid, or an error message
    string if the usage was invalid (meaning nothing should happen except an 
    error would be printed out). The parser will print the appropriate error 
    message if no valid handler is found.   
    """  
    def __init__(self, func=None, verbs=[], trans=False, intrans=False, rstrct=[]):
        self.func = func
        self.verblist = verbs
        self.transitive = trans
        self.intransitive = intrans
        self.restrictions = rstrct
    
    def validate(self, obj):
        for i in self.restrictions:
            if i == 'held':          # if the item must be held by the player to do this Action. TODO: Add more of these rules.
                if i in obj.contents:
                    return True
                else:
                    return False


