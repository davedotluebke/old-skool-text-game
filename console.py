from debug import dbg
from player import Player

class Console:
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
                          }
        self.user = Player(None)

    def set_user(self, cons_user):
        """Set the Player object associated with this console."""
        self.user = cons_user
        
    def write(self, text):
        print(text)

    def loop(self, user):
        while True:
            stop_going = self.parse(user)
            if stop_going:
                break

    def _add_alias(self):
        instructions = 'To create a new alias, type:\n    alias <a> <text>\n' \
                        'where <a> is the new alias and <text> is what will replace the alias.'
        if len(self.words) == 1:
            # print a list of current aliases & instructions for adding
            self.write('Current aliases:')
            
##            sorted = list(self.alias_map)
#3            sorted.sort()   # TODO: figure out how to sort on value rather than key
            for a in sorted(self.alias_map, key=self.alias_map.get):
                self.write('%s --> %s' % (a.rjust(12), self.alias_map[a]))
            self.write(instructions)
            return 
        alias = self.words[1]
        if len(self.words) == 2:
            # print the particular alias if it exists
            if (alias in self.alias_map):
                self.write("'%s' is currently aliased to '%s'" % (alias, self.alias_map[alias]))
            else:
                self.write("'%s' is not currently aliased to anything." % alias)
                self.write(instructions)
            return 
        # new alias specified, insert it into the alias_map
        if (alias in self.alias_map):
            self.write("'%s' is currently aliased to '%s'; changing." % (alias, self.alias_map[alias]))
        expansion = self.last_text.split(maxsplit=2)[2]    # split off first two words and keep the rest
        self.alias_map[alias] = expansion
        self.write("'%s' is now an alias for '%s'" % (alias, expansion))
        return

    def parse(self, user):
        self.last_text = input('-> ')  # store the most recent thing user typed
        
        if self.last_text == 'quit':
            return True
        
        if self.last_text == 'verbose':
            if dbg.verbosity == 0:
                dbg.verbosity = 1
                self.write("Verbose debug output now on.")
            else:
                dbg.verbosity = 0
                self.write("Verbose debug output now off.")
            return False
        
        self.words = self.last_text.split()
        if len(self.words) == 0:
            return False
        
        if self.words[0] == 'alias':
            self._add_alias()         
            return False

        # replace any aliases with their completed version
        self.last_text = ""
        for t in self.words:
            if t in self.alias_map:
                self.last_text += self.alias_map[t] + " "
                dbg.debug("Replacing alias '%s' with expansion '%s'" % (t, self.alias_map[t]))
            else:
                self.last_text += t + " "
        dbg.debug("User input with aliases resolved:\n    %s" % (self.last_text))
        self.words = self.last_text.split()

        sV = self.words[0]   # verb as string
        sDO = None           # Direct object as string
        oDO = None           # Direct object as object
        sIDO = None          # Indirect object as string
        oIDO = None          # Indirect object as object

        num_words = len(self.words)
        a = 0
        while a < num_words:
            dbg.debug('parser: a is %d, self.words[a] is %s' % (a, self.words[a]))
            if self.words[a] in ['a', 'an', 'the']:
                dbg.debug('parser: %s is an article, so removing' % self.words[a])
                del self.words[a]
                num_words = num_words - 1
            a = a + 1

        if (len(self.words) > 1):
            sDO = self.words[1]
        ## TODO: code to remove articles, find prepositions & IDOs, etc
        
        
        possible_nouns = [user.location]           \
                       + [user]                    \
                       + user.contents             \
                       + user.location.contents

        found_matching_noun = False
        found_matching_verb = False
        for i in possible_nouns:
            dbg.debug("parser: possible_nouns includes %s " % (i.id))
            if i.id == sDO:
                dbg.debug("  parser: found a match! Checking whether %s supports verb '%s'" % (i.id, sV))
                found_matching_noun = True
                if sV in i.verb_dict:
                    dbg.debug("    parser: it does! Setting oDO to %s" % (i.id))
                    found_matching_verb = True
                    oDO = i
                    break 
                else:
                    dbg.debug("    parser: it does not! %s probably not the intended direct object." % (i.id))
            else:
                if sV in list(i.verb_dict):
                    dbg.debug("  parser: doesn't match user-typed DO %s, but supports verb %s" % (sDO,sV))
                    found_matching_verb = True
                    if oDO == None:
                        dbg.debug("    parser: setting oDO to %s" % (i.id)) 
                        oDO = i
         
        if oDO:
            verb = oDO.verb_dict[sV]
            dbg.debug("%s . verb_dict[%s]= %s" % (oDO.id, sV, verb))
        else:   # couldn't determine what the verb means
            if (found_matching_noun is True) and (found_matching_verb is False):
                self.write("Sorry, I don't know what that means! (noun '%s' doesn't support verb '%s')" % (sDO,sV))
            elif (found_matching_noun is False) and (found_matching_verb is False): 
                self.write("Sorry, could not find a noun matching '%s' for verb '%s'." % (sDO, sV))
            else:   # this should never happen
                dbg.debug("Parse error, very confused!")
            return False
                
        # all verb functions take console, direct (or invoking) object, indirect object
        verb(self, oDO, oIDO)
        return False

