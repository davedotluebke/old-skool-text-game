from debug import dbg
from player import Player

class Parser:
    def __init__(self):
        self.alias_map = {'n':  'go north',
                          's':  'go south',
                          'e':  'go east', 
                          'w':  'go west', 
                          'nw': 'go northwest',
                          'sw': 'go southwest',
                          'ne': 'go northeast',
                          'se': 'go southeast',
                          'u':  'go up',
                          'd':  'go down',
                          'i':  'inventory',
                          'l':  'look',
                          }
    
    def _add_alias(self, cons, cmd):
        instructions = 'To create a new alias, type:\n    alias <a> <text>\n' \
                        'where <a> is the new alias and <text> is what will replace the alias.'
        if len(self.words) == 1:
            # print a list of current aliases & instructions for adding
            cons.write('Current aliases:')
            for a in sorted(self.alias_map, key=self.alias_map.get):
                cons.write('%s --> %s' % (a.rjust(12), self.alias_map[a]))
            cons.write(instructions)
            return 
        alias = self.words[1]
        if len(self.words) == 2:
            # print the particular alias if it exists
            if (alias in self.alias_map):
                cons.write("'%s' is currently aliased to '%s'" % (alias, self.alias_map[alias]))
            else:
                cons.write("'%s' is not currently aliased to anything." % alias)
                cons.write(instructions)
            return 
        # new alias specified, insert it into the alias_map
        if (alias in self.alias_map):
            cons.write("'%s' is currently aliased to '%s'; changing." % (alias, self.alias_map[alias]))
        expansion = cmd.split(maxsplit=2)[2]    # split off first two words and keep the rest
        self.alias_map[alias] = expansion
        cons.write("'%s' is now an alias for '%s'" % (alias, expansion))
        return

    def diagram_sentence(self, words):
        """Categorize sentence type and set verb, direct/indirect object strings.
        
        Returns a tuple (sV, sDO, sPrep, sIDO)
        sV is a string containing the verb 
        sDO is a string containing the direct object, or None
        sPrep is a string containing the preposition, or None
        sIDO is a string containing the indirect object, or None
        Currently supports three sentence types, which can be detected thus: 
        1.  if sDO == None:     <intransitive verb>
        2.  elif sIDO == None:  <transitive verb> <direct object>
        3.  else:               <transitive verb> <direct object> <preposition> <indirect object>
        """

        sV = words[0]
        if len(self.words) == 1:
            # sentence type 1, <intransitive verb>
            return (sV, None, None, None)

        # list of legal prepositions; note the before-and-after spaces
        prepositions = [' in ', ' on ', ' over ', ' under '] 
        text = ' '.join(words[1:])  # all words after the verb
         
        sDO = sPrep = sIDO = None
        for p in prepositions:
            if p in text:
                (sDO, sPrep, sIDO) = text.partition(p) 
                # break after finding 1st preposition (simple sentences only)
                break  
        if sPrep == None: 
            # no preposition found: Sentence type 2, direct object is all text
            assert(sDO == sIDO == None)  # sDO and sIDO should still be None  
            sDO = text
            return (sV, sDO, sPrep, sIDO)
        # has a preposition: Sentence type 3
        if sDO and sIDO:
            sPrep = sPrep[1:-1]  # strip enclosing spaces
            return (sV, sDO, sPrep, sIDO)
        else:
            dbg.debug("Malformed input: found preposition %s but missing direct object and/or indirect object." % sPrep)
            dbg.debug("Ending a sentence in a preposition is something up with which I will not put.")
            sPrep = sIDO = None
            return (sV, sDO, sPrep, sIDO)
                    
    def parse(self, user, console, command):
        """Parse and enact the user's command. Return True to quit game."""     
        if command == 'quit':
            return True
        
        if command == 'verbose':
            if dbg.verbosity == 0:
                dbg.verbosity = 1
                console.write("Verbose debug output now on.")
            else:
                dbg.verbosity = 0
                console.write("Verbose debug output now off.")
            return False
        
        self.words = command.split()
        if len(self.words) == 0:
            return False
        
        if self.words[0] == 'alias':
            self._add_alias(console, command)         
            return False

        # replace any aliases with their completed version
        command = ""
        for t in self.words:
            if t in self.alias_map:
                command += self.alias_map[t] + " "
                dbg.debug("Replacing alias '%s' with expansion '%s'" % (t, self.alias_map[t]))
            else:
                command += t + " "
        dbg.debug("User input with aliases resolved:\n    %s" % (command))

        self.words = command.split()

        # remove articles:
        num_words = len(self.words)
        a = 0
        while a < num_words:
            dbg.debug('parser: a is %d, self.words[a] is %s' % (a, self.words[a]))
            if self.words[a] in ['a', 'an', 'the']:
                dbg.debug('parser: %s is an article, so removing' % self.words[a])
                del self.words[a]
                num_words = num_words - 1
            a = a + 1

        sV = None            # verb as string
        sDO = None           # Direct object as string
        oDO = None           # Direct object as object
        sIDO = None          # Indirect object as string
        oIDO = None          # Indirect object as object
        sPrep = None         # Preposition as string
        (sV, sDO, sPrep, sIDO) = self.diagram_sentence(self.words)

        # FIRST, search for objects that support the verb the user typed
            # TODO: only include room contents if room is not dark    
        possible_objects = [user.location] + user.contents + user.location.contents + [user]
        possible_verb_objects = []  # list of objects supporting the verb
        possible_verb_actions = []  # corresponding list of actions 
        for obj in possible_objects:
            for act in obj.actions:
                if sV in act.verblist:
                    if (act.intransitive and not sDO) or (act.transitive and sDO): 
                        possible_verb_objects.append(obj)
                        possible_verb_actions.append(act)
        if (not possible_verb_objects): 
            console.write("Parse error: can't find any object supporting verb %s!" % sV)
            return False
        dbg.debug("Parser: Possible objects matching sV '%s': " % ' '.join(o.id for o in possible_verb_objects))
        if not sDO:                 # intransitive verb, no direct object
            verb = possible_verb_actions[0].func
            # all verb functions take parser, console, direct (or invoking) object, indirect object
            verb(self, console, oDO, oIDO)
            return False

        # NEXT, find objects that match the direct & indirect object strings
        matched_objects = []
        if sDO and not sIDO:         # transitive verb + direct object
            sNoun = sDO.split()[-1]  # noun is final word in sDO (after adjectives)
            sAdjectives_list = sDO.split()[:-1]  # all words preceeding noun 
            for obj in possible_objects:
                match = True
                if sNoun in obj.names:
                    for adj in sAdjectives_list:
                        if adj not in obj.adjectives:
                            match = False
                            break
                else:               # sNoun doesn't match any obj.names
                    match = False

                if match:   # name & all adjectives match
                    matched_objects.append(obj)
        dbg.debug("matched_objects are: %s" % ' '.join(obj.id for obj in matched_objects))        
        if not matched_objects:
            console.write("I'm not sure what you mean by "+sDO+".")
            return False 
        elif len(matched_objects) > 1:
            list = ", or ".join(o.short_desc for o in matched_objects)
            console.write("By '%s', do you mean %s?" % (sDO, list))
            return False
        else:   # exactly one object in matched_objects 
            oDO = matched_objects[0]
        
        # if direct object supports the verb, use it
        if oDO in possible_verb_objects:
            act = possible_verb_actions[possible_verb_objects.index(oDO)]
        else:   # otherwise use the first object found to support the verb
            act = possible_verb_actions[0]   
        verb = act.func

        # all verb functions take parser, console, direct (or invoking) object, indirect object
        verb(self, console, oDO, oIDO)
        return False
