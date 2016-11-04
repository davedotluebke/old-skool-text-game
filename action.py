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
    error would be printed out). For example a sword object might support the
    "swing sword" action, but only if the player is holding the sword. In this
    case the action function would return True if the DO object was held by 
    the player, otherwise returning 
        'You can't swing the sword unless you are holding it!'
    This allows the parser to do the right thing, for example, if the user 
    "swing sword" when you are holding one sword while another is in the room.  
    """  
    def __init__(self, func=None, verbs=[], trans=False, intrans=False):
        self.func = func
        self.verblist = verbs
        self.transitive = trans
        self.intransitive = intrans