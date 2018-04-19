import sys
import traceback
import os.path

import gametools

from debug import dbg
from container import Container
from player import Player

class Parser:
    ordinals = {"first":1, "second":2, "third":3, "fourth":4, "fifth":5, "sixth":6, "seventh":7, "eighth":8, "ninth":9, "tenth":10}
    def _set_verbosity(self, level=-1):
        if level != -1:
            dbg.verbosity = level
            return "Verbose debug output now %s, verbosity level %s." % ('on' if level else 'off', dbg.verbosity)
        if dbg.verbosity == 0:
            dbg.verbosity = 1
            return "Verbose debug output now on, verbosity level %s." % dbg.verbosity
        else:
            dbg.verbosity = 0
            return "Verbose debug output now off."

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
        prepositions = ['in', 'on', 'over', 'under', 'with', 'at', 'from', 'off', 'out', 'into', 'away', 'around', 'onto'] 
        textwords = words[1:]  # all words after the verb
        text = ' '.join(textwords)  
        
        sDO = sPrep = sIDO = None
        for p in prepositions:
            if p in textwords:
                if sV == 'go' and p == 'in':  # what is this doing? 
                    continue
                idxPrep = textwords.index(p)
                sPrep = textwords[idxPrep]
                sDO = ' '.join(textwords[:idxPrep])
                sIDO = ' '.join(textwords[idxPrep+1:])
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
        if not sIDO: 
            dbg.debug("Possibly malformed input: found preposition %s but missing indirect object." % sPrep)
            dbg.debug("Ending a sentence in a preposition is something up with which I will not put.")
        return (sV, sDO, sPrep, sIDO)

    def _find_matching_objects(self, sObj, objs, cons):
        """Find an object in the list <objs> matching the given string <sObj>.
        Tests the name(s) and any adjectives for each object in <objs> against the words in sObj. 
        
        Returns the matching object or None if 1 or 0 objects match sObj.

        Returns False after writing an error message to Console <cons> if more than 1 object matches. """
        matched_objects = []
        sNoun = sObj.split()[-1]  # noun is final word in sObj (after adjectives)
        sAdjectives_list = sObj.split()[:-1]  # all words preceeding noun
        # In case multiple objects match the noun and adjectives given, 
        # player may specify an ordinal adjective ('first', 'second', ..). 
        ord_number = 0  # which ordinal (first=1,second=2,..), 0 if none specified
        ord_str = ""    # actual string used to specify ordinal ('first', '3rd', etc)
        for obj in objs:
            match = True
            if sNoun in obj.names:
                for adj in sAdjectives_list:
                    if adj in Parser.ordinals:  # dict mapping ordinals->ints
                        if ord_str and ord_str != adj: 
                            cons.write("I'm confused: you specified both %s and %s!" % (ord_str, adj))
                            return False
                        ord_number = Parser.ordinals[adj]
                        ord_str = adj
                    elif adj not in obj.adjectives:
                        match = False  # found an invalid adjective
                        break
            else: 
                match = False  # sNoun doesn't match any obj.names

            # if name & all adjectives match, add to list of matching objects
            if match: 
                matched_objects.append(obj)
        if ord_number:  
            try:
                matched_objects = [matched_objects[ord_number - 1]]
            except IndexError:
                cons.write("You specified '%s' but I only see %d objects matching %s %s!" % (ord_str, len(matched_objects), ' '.join(x for x in sAdjectives_list if x not in Parser.ordinals), sNoun))
                return False
        dbg.debug("matched_objects are: %s" % ' '.join(obj.id for obj in matched_objects), 3)        
        if len(matched_objects) > 1:
            candidates = ", or the ".join(o.short_desc for o in matched_objects)
            cons.write("By '%s', do you mean the %s? Please provide more adjectives, or specify 'first', 'second', 'third', etc." % (sObj, candidates))
            return False
        elif len(matched_objects) == 0:
            # user typed a direct object that doesn't match any objects. Could be 
            # an error, could be e.g. "go north". Validate all supporting objects.
            return None
        else:   # exactly one object in matched_objects 
            return matched_objects[0]

    def parse(self, user, console, command):
        """Parse and enact the user's command. Return False to quit game."""
        dbg.debug("parser called (user='%s', command='%s', console=%s)" % (user, command, console))
        if command == 'quit':
            console.game.save_player(os.path.join(gametools.PLAYER_DIR, user.names[0]), user)
            console.write("#quit")
            return False

        if command == 'quit game':
            console.game.keep_going = False
        
        self.words = command.split()
        if len(self.words) == 0:
            if user.reading == True:
                self.words = ["read", "next", "page"]
            else:
                return True

        if self.words[0] == 'verbose':
            try:
                level = int(self.words[1])
            except IndexError:
                console.write(self._set_verbosity())
                return True
            except ValueError:
                if self.words[1] == 'filter':
                    try:
                        s = self.words[2:] 
                        dbg.set_filter_str(s)
                        console.write("Set verbose filter to '%s', debug strings containing '%s' will now be printed." % (s, s))                      
                    except IndexError:
                        dbg.set_filter_str('&&&')
                        console.write("Turned off verbose filter; debug messages will only print if they are below level %d." % dbg.verbosity)
                    return True
                console.write("Usage: verbose [level]\n    Toggles debug message verbosity on and off (level 1 or 0), or sets it to the optionally provided <level>")
                return True
            console.write(self._set_verbosity(level))
            return True
        
        # remove articles and convert to lowercase, unless the command 
        # requires the exact user text:
        if self.words[0] not in ['execute', 'say', 'shout', 'whisper', 'mutter', 'emote']:
            command = command.lower()   
            self.words = [w for w in self.words if w not in ['a', 'an', 'the']]
            if len(self.words) == 0:
                console.write("Please specify more than just articles!")
                return True

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
            if isinstance(obj, Container) and obj.see_inside and obj is not user:
                possible_objects += obj.contents
        
        possible_verb_objects = []  # list of objects supporting the verb
        possible_verb_actions = []  # corresponding list of actions 
        for obj in possible_objects:
            for act in obj.actions:
                if sV in act.verblist:
                    if (act.intransitive and not sDO) or (act.transitive): 
                        possible_verb_objects.append(obj)
                        possible_verb_actions.append(act)
        if (not possible_verb_objects): 
            if sDO == None:
                console.write("Parse error: can't find any object supporting intransitive verb %s!" % sV)
            else:
                console.write("Parse error: can't find any object supporting transitive verb %s!" % sV)
            # TODO: more useful error messages, e.g. 'verb what?' for transitive verbs 
            return True
        dbg.debug("Parser: Possible objects matching sV '%s': " % ' '.join(o.id for o in possible_verb_objects), 3)

        # NEXT, find objects that match the direct & indirect object strings    
        if sDO: 
            oDO = self._find_matching_objects(sDO, possible_objects, console)
        if sIDO: 
            oIDO = self._find_matching_objects(sIDO, possible_objects, console)
        if oDO == False or oIDO == False: 
            return True     # ambiguous user input; >1 object matched 
         
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
            if (user.game.handle_exceptions):
                try:
                    result = act.func(self, console, oDO, oIDO) # <-- ENACT THE VERB
                except Exception as isnt:
                    console.write('An error has occured. Please try a different action until the problem is resolved.')
                    dbg.debug(traceback.format_exc(), 0)
                    dbg.debug("Error caught!", 0)
                    result = True       # we don't want the parser to go and do an action they probably didn't intend
            else:
                result = act.func(self, console, oDO, oIDO)  # <-- ENACT THE VERB
            if result == True:      # mean to do if there is a bug in the one they did mean to do
                break               # verb has been enacted, all done!
            if err_msg == None: 
                err_msg = result    # save the first error encountered

        if result == True:
            return True

        # no objects handled the verb; print the first error message 
        console.write(err_msg if err_msg else "No objects handled verb, but no error message defined!")
        return True

