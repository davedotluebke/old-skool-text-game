from debug import dbg

class Action:
    """An action the player can do, associated with an object in the game.
    Specifies a function <func> which is enacted by the player using one or more 
    verb synonums (strings in <verblist>).  Verbs can be <transitive> (taking a 
    direct object), <intransitive> (no direct object), or both.
    
    Action functions take the special form 
        a(parser, console, DO, IDO, validate)
    where parser and console are from the current client, DO is the object 
    that the parser has determined is the direct object of the user's command
    (or None if the verb is intransitive), IDO is the indirect object (if any),
    and validate is a Boolean indicating whether the verb is to be enacted or 
    just 'validated'. If validate is True the action function returns True if  
    the verb, DO (if any), and IDO (if any) make a valid construction, and 
    returns an error message otherwise. For example a sword object might 
    support the "swing sword" action, but only if the player is holding the
    sword. In this case the 'validate' mode of the action function would return
    True if the DO object was held by the player, otherwise returning 
        'You can't swing the sword unless you are holding it!'
    The validate mode is used by the parser to eliminate possible nouns, for 
    example to do the right thing if type "swing sword" when you are holding 
    one sword while another is in the room.  
    """  
    def __init__(self, func=None, verbs=[], trans=False, intrans=False):
        self.func = func
        self.verblist = verbs
        self.transitive = trans
        self.intransitive = intrans