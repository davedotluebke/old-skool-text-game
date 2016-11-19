from debug import dbg
from container import Container
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

    def _replace_aliases(self):
        cmd = ""
        for t in self.words:
            if t in self.alias_map:
                cmd += self.alias_map[t] + " "
                dbg.debug("Replacing alias '%s' with expansion '%s'" % (t, self.alias_map[t]))
            else:
                cmd += t + " "
        dbg.debug("User input with aliases resolved:\n    %s" % (cmd))
        return cmd

    def _toggle_verbosity(self, cons):
        if dbg.verbosity == 0:
            dbg.verbosity = 1
            cons.write("Verbose debug output now on.")
        else:
            dbg.verbosity = 0
            cons.write("Verbose debug output now off.")

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

        # list of legal prepositions
        prepositions = ['in', 'on', 'over', 'under', 'with', 'at', 'from', 'off'] 
        textwords = words[1:]  # all words after the verb
        text = ' '.join(textwords)  
        
        sDO = sPrep = sIDO = None
        for p in prepositions:
            if p in textwords:
                if sV == 'go' and p == 'in':
                    continue
                idxPrep = textwords.index(p)
                sPrep = textwords[idxPrep]
                sDO = ' '.join(textwords[:idxPrep])
                sIDO = ' '.join(textwords[idxPrep+1:])
                # old style: (sDO, sPrep, sIDO) = text.partition(p) 
                # break after finding 1st preposition (simple sentences only)
                break  
        if sPrep == None: 
            # no preposition found: Sentence type 2, direct object is all text
            assert(sDO == sIDO == None)  # sDO and sIDO should still be None  
            sDO = text
            return (sV, sDO, sPrep, sIDO)
        # has a preposition: Sentence type 3 or 4
        if sDO == "": sDO = None
        if sIDO == "": sIDO = None
        if sIDO: 
            return (sV, sDO, sPrep, sIDO)
        else:
            dbg.debug("Malformed input: found preposition %s but missing indirect object." % sPrep)
            dbg.debug("Ending a sentence in a preposition is something up with which I will not put.")
            sPrep = sIDO = None
            return (sV, sDO, sPrep, sIDO)

    def _find_matching_objects(self, sObj, objs, cons):
        """Find an object in the list <objs> matching the given string <sObj>.
        Tests the name(s) and any adjectives for each object in <objs> against the words in sObj. 
        
        Returns the matching object or None if 1 or 0 objects match sObj.

        Returns False after writing an error message to Console <cons> if more than 1 object matches. """
        matched_objects = []
        sNoun = sObj.split()[-1]  # noun is final word in sObj (after adjectives)
        sAdjectives_list = sObj.split()[:-1]  # all words preceeding noun 
        for obj in objs:
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
        if len(matched_objects) > 1:
            candidates = ", or ".join(o.short_desc for o in matched_objects)
            cons.write("By '%s', do you mean %s?" % (sObj, candidates))
            return False
        elif len(matched_objects) == 0:
            # user typed a direct object that doesn't match any objects. Could be 
            # an error, could be e.g. "go north". Validate all supporting objects.
            return None
        else:   # exactly one object in matched_objects 
            return matched_objects[0]

    def parse(self, user, console, command):
        """Parse and enact the user's command. Return False to quit game."""     
        command = command.lower()   # convert whole string to lowercase
        if command == 'quit': 
            return False
        
        if command == 'verbose':
            self._toggle_verbosity(console)
            return True
        
        self.words = command.split()
        if len(self.words) == 0:
            return True
        
        if self.words[0] == 'alias':
            self._add_alias(console, command)         
            return True

        # replace any aliases with their completed version
        command = self._replace_aliases()
        self.words = command.split()

        # remove articles:
        self.words = [w for w in self.words if w not in ['a', 'an', 'the']]

        sV = None            # verb as string
        sDO = None           # Direct object as string
        oDO = None           # Direct object as object
        sIDO = None          # Indirect object as string
        oIDO = None          # Indirect object as object
        sPrep = None         # Preposition as string
        (sV, sDO, sPrep, sIDO) = self.diagram_sentence(self.words)

        # FIRST, search for objects that support the verb the user typed
            # TODO: only include room contents if room is not dark (but always include user)
        possible_objects = [user.location] 
        for obj in user.contents + user.location.contents:
            possible_objects += [obj]
            if isinstance(obj, Container) and obj.see_inside and obj is not console.user:
                possible_objects += obj.contents
        
        possible_verb_objects = []  # list of objects supporting the verb
        possible_verb_actions = []  # corresponding list of actions 
        for obj in possible_objects:
            for act in obj.actions:
                if sV in act.verblist:
                    if (act.intransitive and not sDO) or (act.transitive and sDO): 
                        possible_verb_objects.append(obj)
                        possible_verb_actions.append(act)
        if (not possible_verb_objects): 
            if sDO == None:
                console.write("Parse error: can't find any object supporting intransitive verb %s!" % sV)
            else:
                console.write("Parse error: can't find any object supporting transitive verb %s!" % sV)
            # TODO: more useful error messages, e.g. 'verb what?' for transitive verbs 
            return True
        dbg.debug("Parser: Possible objects matching sV '%s': " % ' '.join(o.id for o in possible_verb_objects))

        # NEXT, find objects that match the direct & indirect object strings    
        if sDO: 
            oDO = self._find_matching_objects(sDO, possible_objects, console)
        if sIDO: 
            oIDO = self._find_matching_objects(sIDO, possible_objects, console)
        if oDO == False or oIDO == False: 
            return True     # ambiguous user input; >1 object matched 

        if not sDO:                 # intransitive verb, no direct object
            verb = possible_verb_actions[0].func
            # all verb functions take parser, console, direct (or invoking) object, indirect object
            verb(self, console, oDO, oIDO)
            return True
         
        # If direct or indirect object supports the verb, try first in that order
        initial_actions = []
        for o in (oDO, oIDO):
            if o in possible_verb_objects:
                idx = possible_verb_objects.index(o)
                initial_actions.append(possible_verb_actions[idx])
        possible_verb_actions = initial_actions + possible_verb_actions
                
        # Try the "verb functions" associated with each object/action pair.
        # If a valid usage of this verb function, it will return True and 
        # the command has been handled; otherwise it returns an error message. 
        # In this case keep trying other actions. If no valid verb function is 
        # found, print the error message from the first invalid verb tried.   
        result = False
        err_msg = None
        for act in possible_verb_actions:
            result = act.func(self, console, oDO, oIDO) # <-- ENACT THE VERB
            if result == True:
                break               # verb has been enacted, all done!
            if err_msg == None: 
                err_msg = result    # save the first error encountered

        if result == True:
            return True

        # no objects handled the verb; print the first error message 
        console.write(err_msg)
        return True

