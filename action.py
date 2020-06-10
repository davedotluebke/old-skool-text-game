from collections import namedtuple

Action = namedtuple('Action', ['func', 'trans', 'intrans'])
"""An action the player can do, associated with an object in the game or
with a class of objects.  Specifies an action function <func> which is
to be enacted when the player types a verb mapped to this Action. Verbs
can be transitive, taking a direct object (<trans> == True); intransitive,
with no direct object (<intrans> == True); or both.

Action functions always take the special form 
    a(parser, console, DO, IDO)
where parser and console are from the current client, DO is the object 
that the parser has determined is the direct object of the user's command
(or None if the verb is intransitive), IDO is the indirect object (if any). 
Action functions return True if the usage was valid, or an error message
string if the usage was invalid (meaning nothing should happen except an 
error would be printed out). The parser will print the appropriate error 
message if no valid handler is found.   
"""  

