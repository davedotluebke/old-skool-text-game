import sys
import traceback

import gametools

from debug import dbg
from container import Container
from player import Player

class Parser:
    ordinals = {"first":1, "second":2, "third":3, "fourth":4, "fifth":5, "sixth":6, "seventh":7, "eighth":8, "ninth":9, "tenth":10,
                "1st":1, "2nd":2, "3rd":3, "4th":4, "5th":5, "6th":6, "7th":7, "8th":8, "9th":9, "10th":10}

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
            # no preposition found: Sentence type 2, direct object is `text`
            assert(sDO == sIDO == None)  # sDO and sIDO should still be None  
            sDO = text
            return (sV, sDO, sPrep, sIDO)
        # has a preposition: Sentence type 1 or 3
        if sDO == "": sDO = None    # no direct object
        if sIDO == "": sIDO = None  # no indirect object 
        if not sIDO: 
            dbg.debug("Possibly malformed input: found preposition %s but missing indirect object." % sPrep)
            dbg.debug("Ending a sentence in a preposition is something up with which I will not put.")
        return (sV, sDO, sPrep, sIDO)

    def _find_matching_objects(self, sObj, objs, cons):
        """Find an object in the list <objs> matching the given string <sObj>.
        Tests the name(s) and any adjectives for each object in <objs> against the words in sObj. 
        
        Returns the matching object if 1 object matches sObj.
        Returns None if 0 objects match sObj.
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
            # count through all matched objects, some of which might be plural
            i = 1                   # ordinals start at "first" meaning element 0
            for o in matched_objects:
                i += o.plurality    # singular objects have plurality == 1
                if ord_number < i:  
                    matched_objects = [o]  # ordinal specifies an object in this plurality
                    break
            else:  # for-else clause, runs if no break called in loop
                cons.write("You specified '%s' but I only see %d %s matching '%s %s'!" % (
                    ord_str, 
                    i-1, 
                    'objects' if i-1 > 1 else 'object', 
                    ' '.join(x for x in sAdjectives_list if x not in Parser.ordinals), 
                    sNoun))
                return False
        dbg.debug("matched_objects are: %s" % ' '.join(obj.id for obj in matched_objects), 3)        
        if len(matched_objects) > 1:
            candidates = ", or the ".join(o._short_desc for o in matched_objects)
            cons.write("By '%s', do you mean the %s? Please provide more adjectives, or specify 'first', 'second', 'third', etc." % (sObj, candidates))
            return False
        elif len(matched_objects) == 0:
            # user typed a direct object that doesn't match any objects. Could be 
            # an error, could be e.g. "go north". Validate all supporting objects.
            return None
        else:   # exactly one object in matched_objects 
            return matched_objects[0]

    def parse(self, user, console, command):
        """Parse and enact the user's command. """
        dbg.debug("parser called (user='%s', command='%s', console=%s)" % (user, command, console))
        
        self.words = command.split()
        if len(self.words) == 0:
            return True

        if self.words[0] == 'verbose':
            self._handle_verbose(console)
        
        # remove articles and convert to lowercase, except for some commands that 
        # treat everything after the verb as a single "diect object" string
        # (TODO: directly recognise strings delimited by '' or ")
        if self.words[0].lower() not in ['execute', 'say', 'shout', 'whisper', 'mutter', 'emote']:
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
        # (only include room contents if room is not dark (but always include user)
        room = user.location
        possible_objects = [room] 
        for obj in user.contents + ([] if room.is_dark() else room.contents):
            possible_objects += [obj]
            if isinstance(obj, Container) and obj.see_inside and obj is not user:
                possible_objects += obj.contents

        # THEN, check for objects matching the direct & indirect object strings
        if sDO: 
            oDO = self._find_matching_objects(sDO, possible_objects, console)
        if sIDO: 
            oIDO = self._find_matching_objects(sIDO, possible_objects, console)
        if oDO == False or oIDO == False: 
            return True     # ambiguous user input; >1 object matched 

        # NEXT, find objects that support the verb the user typed
        possible_verb_objects = []  # list of objects supporting the verb
        for obj in possible_objects:
            act = obj.actions.get(sV)  # returns None if <sV> not in <actions>
            if act and ((act.intrans and not sDO) or (act.trans)): 
                possible_verb_objects.append(obj)
        if (not possible_verb_objects): 
            console.write("Parse error: can't find any object supporting "
                            + ('intransitive' if sDO == None else 'transitive')
                             + " verb %s!" % sV)
            # TODO: more useful error messages, e.g. 'verb what?' for transitive verbs 
            return True
        dbg.debug("Parser: Possible objects matching sV '%s': " % ' '.join(o.id for o in possible_verb_objects), 3)

        # If direct or indirect object supports the verb, try first in that order
        p = possible_verb_objects  # terser reference to possible_verb_objects
        if oIDO in p:
            p.insert(0, p.pop(p.index(oIDO)))  # swap oIDO to front of p
        if oDO in p:
            p.insert(0, p.pop(p.index(oDO)))   # swap oDO to front of p
                
        # FINALLY, try the action ("verb functions") of each object we found. 
        # If a valid usage of this verb function, it will return True and 
        # the command has been handled; otherwise it returns an error message. 
        # In this case keep trying other actions. If no valid verb function is 
        # found, print the error message from the first invalid verb tried.   
        result = False
        err_msg = None
        for obj in possible_verb_objects:
            #  If obj is plural, peel off extra copies before trying to enact the verb
            # TODO: support peeling off a plurality, e.g. "drop three coins"
            plural = obj.plurality > 1
            if plural:  
                obj_copy = obj.replicate()
                obj_copy.plurality = obj.plurality - 1
                obj.plurality = 1
            # Check direct/indirect object plurality, peel off extra copies. 
            # Note: often oDO or oIDO points to obj, so test this after un-pluralizing obj
            oDO_plural = (oDO.plurality > 1) if oDO else False
            if oDO_plural:  
                oDO_copy = oDO.replicate()
                # TODO: support peeling off a plurality, e.g. "drop three coins"
                oDO_copy.plurality = oDO.plurality - 1
                oDO.plurality = 1
            oIDO_plural = (oIDO.plurality > 1) if oIDO else False
            if oIDO_plural:
                oIDO_copy = oIDO.replicate()
                # TODO: support peeling off a plurality, e.g. "drop three coins"
                oIDO_copy.plurality = oIDO.plurality - 1
                oIDO.plurality = 1
            
            act = obj.actions[sV]
            try:
                result = act.func(obj, self, console, oDO, oIDO) # <-- ENACT THE VERB
            except Exception as isnt:
                console.write('An error has occured. Please try a different action until the problem is resolved.')
                dbg.debug(traceback.format_exc(), 0)
                dbg.debug("Error caught!", 0)
                if plural: 
                    obj.plurality += obj_copy.plurality 
                    obj_copy.destroy()
                if oDO_plural:
                    oDO.plurality += oDO_copy.plurality
                    oDO_copy.destroy()
                if oIDO_plural:
                    oIDO.plurality += oIDO_copy.plurality
                    oIDO_copy.destroy()
                result = True   # we don't want the parser to go and do an action they probably didn't intend
            if plural:
                # did the action change obj so we need to remove from plurality?
                if obj.is_identical_to(obj_copy):  
                    # no, obj_copy is identical to obj, merge back into a single plurality
                    obj.plurality += obj_copy.plurality 
                    obj_copy.destroy()
                else:
                    # yes, obj_copy remains, register heartbeat for obj_copy if needed
                    if obj in Container.game.heartbeat_users:
                        Container.game.register_heartbeat(obj_copy)
            if oDO_plural:
                # did the action change oDO so we need to remove from plurality?
                if oDO.is_identical_to(oDO_copy):  
                    # no, oDO_copy is identical to oDO, merge back into a single plurality
                    oDO.plurality += oDO_copy.plurality 
                    oDO_copy.destroy()
                else:
                    # yes, oDO_copy remains, register heartbeat for oDO_copy if needed
                    if oDO in Container.game.heartbeat_users:
                        Container.game.register_heartbeat(oDO_copy)
            if oIDO_plural:
                # did the action change oIDO so we need to remove from plurality?
                if oIDO.is_identical_to(oIDO_copy):  
                    # no, oIDO_copy is identical to oIDO, merge back into a single plurality
                    oIDO.plurality += oIDO_copy.plurality 
                    oIDO_copy.destroy()
                else:
                    # yes, oIDO_copy remains, register heartbeat for oIDO_copy if needed
                    if oIDO in Container.game.heartbeat_users:
                        Container.game.register_heartbeat(oIDO_copy)
            
            if result == True:
                break               # verb has been enacted, all done!
            if err_msg == None: 
                err_msg = result    # save the first error encountered

        if result != True:
            # no objects handled the verb; print the first error message 
            console.write(err_msg if err_msg else "No objects handled verb, but no error message defined!")

        return True

