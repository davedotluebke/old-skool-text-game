import sys
import traceback
import re

import gametools

from debug import dbg
from container import Container
from player import Player

class Parser:
    ordinals = {"first":1, "second":2, "third":3, "fourth":4, "fifth":5, "sixth":6, "seventh":7, "eighth":8, "ninth":9, "tenth":10,
                "1st":1, "2nd":2, "3rd":3, "4th":4, "5th":5, "6th":6, "7th":7, "8th":8, "9th":9, "10th":10}

    def _split_and_simplify(self, s):
        """Split command into words using whitespace, remove articles
        ('a' and 'the'), and convert to lowercase -- but don't modify 
        "strings" of text between quotes; treat these as 1 word.  More
        precisely: treat the contents of any string literals (sequences 
        of text demarcated with the double-quote `"` character) as a 
        single word with the demarcation characters stripped. Thus if `s` 
        consists of:
            Tell the troll "Let me pass!"
        the function will return:
            ['Tell', 'the', 'troll', 'Let me pass!']
        The final `"` is actually optional, and no word will be returned 
        for empty strings. Note that we only support `"` to demarcate strings,
        not `'`. Nor does this function handle nesting of strings: If a
        string literal demarcated with `"` contains a nested string 
        demarcated with `'`, that nested string is simply treated as part 
        of the encompassing string's single "word". This is helpful for the
        wizardly 'execute' command, which allows the wizard to type valid 
        Python commands to execute in the parser--by using `'` to indicate 
        strings inside the command, the wizard avoids escaping quotation
        marks. TODO: support escaping quotes with the backslash character."""
        words = []
        sections = s.split('"')  # split s into sections inside & outside quotes
        numsections = len(sections)
        # Odd-numbered sections are between quotes, e.g <section[0] "section[1]" section[2] "section[3]">:
        #   put everything between the quotes into a single word.
        # Even-numbered sections are outside quotes (including section[0] when are no quotes):
        #   split these sections into words according to whitespace.
        for i in range(numsections):      
            if sections[i]:  # skip empty sections
                if i & 0x1:  # if i is odd (lowest bit set), add section directly as a word
                    words += [sections[i]]
                else:  # i is even: convert to lowercase, split by whitespace, strip articles
                    words += [w for w in sections[i].lower().split() if w not in ['a', 'an', 'the']]
        return words

    def diagram_sentence(self, words):
        """Categorize sentence type and set verb, direct/indirect object strings.
        
        Returns a tuple (sV, sDO, sPrep, sIDO)
        sV is a string containing the verb 
        sDO is a list of strings containing the direct object(s), or None
        sPrep is a string containing the preposition, or None
        sIDO is a list of strings containing the indirect object(s), or None
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

    def find_matching_objects(self, sObj, objs, cons):
        """Find object(s) in the list <objs> matching the given string <sObj>.
        Tests the name(s) and any adjectives for each object in <objs> against the words in sObj.
        sObj may be a compound object, with multiple "object specifiers", for example 
        "rusty sword, ten gold coins, and third pink potion". In this case the function will
        return a list of matching objects, splitting plural objects as needed. 
        XXX SPLITTING PLURALITIES NOT YET IMPLEMENTED
                
        Returns a list with:
          - the matching object, if 1 object (which may be a plurality) matches sObj.
          - all matching objects, if <sObj> unambiguously specifies multiple objects.
        Returns [] (empty list) if 0 objects match sObj (or any of the specifiers).
        Returns False after writing an error message to <cons> if any specifier ambiguously matches multiple objects."""
        matched_objects = []
        # Build list of object 'specifier' strings, separated by commas and/or 'and'
        # split on regexp for commas, "and"s, &s. Should be cached, no need to compile
        lsObj = re.split("and\s+|,\s*|and,\s*|\&\s*", sObj)  
        for s in lsObj:  # loop over specifiers, trying to match each to an object
            local_matches = []  # each specifier should be just one object, though it may be plural
            if not s:
                continue  # skip over blank  strings
            sWords = s.split()
            sNoun = sWords[-1]  # noun is final word in specifier string (after adjectives)
            sAdjectives_list = sWords[:-1]  # all words preceeding noun
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
                    local_matches.append(obj)
            # if they specified an ordinal (1st, 2nd, etc), figure out which object they meant
            if ord_number:  
                # count through all matched objects, some of which might be plural
                i = 1                   # ordinals start at "first" meaning element 0
                for o in local_matches:
                    i += o.plurality    # singular objects have plurality == 1
                    if ord_number < i:  
                        local_matches = [o]  # ordinal specifies an object in this plurality
                        break
                else:  # for-else section, runs if no break called in loop
                    cons.write("You specified '%s' but I only see %d %s matching '%s %s'!" % (
                        ord_str, 
                        i-1, 
                        'objects' if i-1 > 1 else 'object', 
                        ' '.join(x for x in sAdjectives_list if x not in Parser.ordinals), 
                        sNoun))
                    return False
            dbg.debug("local_matches in '%s' are: %s" % (s, ' '.join(obj.id for obj in local_matches)), 3)        
            if len(local_matches) > 1:
                candidates = ", or the ".join(o._short_desc for o in local_matches)
                cons.write("By '%s', do you mean the %s? Please provide more adjectives, or specify 'first', 'second', 'third', etc." % (s, candidates))
                return False
            elif len(local_matches) == 0:
                # user typed an object specifier that doesn't match any objects. Could be 
                # an error, could be e.g. "go north". Validate all supporting objects.
                return []
            else:   # exactly one object in local_matches 
                matched_objects += local_matches
        
        dbg.debug("matched_objects in '%s' are: %s" % (sObj, ' '.join(obj.id for obj in matched_objects)), 3)
        return matched_objects

    def _try_verb_from_obj(self, sV, obj, oDO, oIDO, cons):
        """Try the action function matching the verb `sV` for an object `obj`. 
        Passes on the direct object `oDO` and indirect object `oIDO` as well as
        the parser and console. The action function returns True to indicate 
        this is a valid usage of the verb function and the appropriate action
        has been performed; otherwise it returns an error message string.

        If obj, oDO, or oIDO are plural, peel off a singular copy before 
        trying to enact the verb, then afterwards compare the enacted object
        to the remaining copies to see if the action has changed the object. 
        If not, merge the unchanged object back into the plurality. 
        """
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
        try:  ### ENACT THE VERB ###
            result = act.func(obj, self, cons, oDO, oIDO) 
        except Exception:  # error, roll back any plurality changes and return True
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
            result = True   # upon error, don't go do a different action - user probably intended this one
        if plural:  # did the action change obj so we need to remove from plurality?
            if obj.is_identical_to(obj_copy):  
                # no, obj_copy is identical to obj, merge back into a single plurality
                obj.plurality += obj_copy.plurality 
                obj_copy.destroy()
            else:
                # yes, obj_copy remains, register heartbeat for obj_copy if needed
                if obj in Container.game.heartbeat_users:
                    Container.game.register_heartbeat(obj_copy)
        if oDO_plural:  # did the action change oDO so we need to remove from plurality?                
            if oDO.is_identical_to(oDO_copy):  
                # no, oDO_copy is identical to oDO, merge back into a single plurality
                oDO.plurality += oDO_copy.plurality 
                oDO_copy.destroy()
            else:
                # yes, oDO_copy remains, register heartbeat for oDO_copy if needed
                if oDO in Container.game.heartbeat_users:
                    Container.game.register_heartbeat(oDO_copy)
        if oIDO_plural:  # did the action change oIDO so we need to remove from plurality?
            if oIDO.is_identical_to(oIDO_copy):  
                # no, oIDO_copy is identical to oIDO, merge back into a single plurality
                oIDO.plurality += oIDO_copy.plurality 
                oIDO_copy.destroy()
            else:
                # yes, oIDO_copy remains, register heartbeat for oIDO_copy if needed
                if oIDO in Container.game.heartbeat_users:
                    Container.game.register_heartbeat(oIDO_copy)
        return result

    def parse(self, user, console, command):
        """Parse and enact the user's command. Valid commands have the form:
            <verb> [direct object(s)] [preposition   indirect object(s)]
        If multiple different direct objects are specified (as opposed to 
        a plurality of one kind of object, e.g. "ten gold coins"), enact the 
        verb on each direct object in turn, passing the full list of indirect
        objects (if any) each time. 
        """
        dbg.debug("parser called (user='%s', command='%s', console=%s)" % (user, command, console), 3)
        
        # Split command into words, remove articles, convert to lowercase--but
        # don't modify "strings" of text between quotes; treat these as 1 word
        self.words = self._split_and_simplify(command)

        if len(self.words) == 0:
            return True
        
        sV = None            # verb as string
        sDO = None           # Direct object as string
        oDO_list = []        # List of direct object(s) as object
        sIDO = None          # Indirect object as string
        oIDO_list = []       # List of indirect object(s) as object
        sPrep = None         # Preposition as string
        (sV, sDO, sPrep, sIDO) = self.diagram_sentence(self.words)

        # FIRST, search for objects that support the verb the user typed
        # (only include room contents if room is not dark (but always include user)
        room = user.location
        possible_objects = [room] 
        for obj in user.contents + (None if room.is_dark() else room.contents):  
            possible_objects += [obj]
            if isinstance(obj, Container) and obj.see_inside and obj is not user:
                possible_objects += obj.contents

        # THEN, check for objects matching the direct & indirect object strings
        if sDO:   # set oDO to object(s) matching direct object strings
            oDO_list = self.find_matching_objects(sDO, possible_objects, console)
        if sIDO:  # set oDO to object(s) matching direct object strings
            oIDO_list = self.find_matching_objects(sIDO, possible_objects, console)
        if oDO_list == False or oIDO_list == False:
            return True     # ambiguous user input; >1 object matched or multiple DOs _and_ IDOs matched
        
        # NEXT, find objects that support the verb the user typed. 
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

        # If multiple direct or indirect objects, enact the verb on each in turn.
        # See discussion in issue #89: the correct verb function (action) could come from 
        # the direct objects ("take sword and bow from chest", `take()`` from `Thing`), the
        # indirect object ("put sword and bow in chest", `put()` from `Container`), or some 
        # unnamed object ("attack troll" engaging `attack` in a wielded `Weapon`). Solution:
        #
        # First try enacting the action from a direct object on itself. 
        #   If successful, enact the verbs from any other direct objects on themselves in turn.  
        # If not, test the verbs from the indirect object, then all other possible objects
        #   If any of these verbs succeeds, use the SAME verb on any other direct objects. 

        # move direct and indirect objects to the front of the list:
        p = possible_verb_objects  # terser 
        p = oDO_list + oIDO_list + [o for o in p if o not in oDO_list and o not in oIDO_list]
                
        err_msg = None
        result = False
        oDO = oDO_list[0] if oDO_list else None     # Try the first direct object (if any) first
        oIDO = oIDO_list[0] if oIDO_list else None  # XXX compound indirect objects not yet supported
        # FINALLY, try the actions ("verb functions") of each object until
        # one returns True (indicating the action was handled). If an action
        # returns an error message instead, keep trying other actions. If no
        # object's action returns True, print the first object's error message.
        for obj in p:
            result = self._try_verb_from_obj(sV, obj, oDO, oIDO, console)
            
            if result == True:  # verb from obj successfully enacted! 
                if obj in oDO_list:  # was it a direct object? 
                    for d in oDO_list[1:] : # if so, enact the verb from all the other DOs on themselves
                        result = self._try_verb_from_obj(sV, d, d, oIDO, console)
                        if result != True:
                            break  # this direct object failed even though others succeeded, abort here
                else:  # verb supported by an indirect object or unnamed object
                    for d in oDO_list[1:] :  # enact the SAME verb on every direct object
                        result = self._try_verb_from_obj(sV, obj, d, oIDO, console)
                        if result != True:
                            break  # this direct object failed even though others succeeded, abort here
                break  # verb has been enacted by at least one object, all done!
            if err_msg == None: 
                err_msg = result    # save the first error encountered

        if result != True:
            # no objects handled the verb; print the first error message 
            console.write(err_msg if err_msg else "No objects handled verb, but no error message defined!")

        return True

