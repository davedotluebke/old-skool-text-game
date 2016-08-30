from thing import *
from container import *
from room import *
from creature import *
from player import *

class Console:
    def __init__(self):
        self.user = Player("testplayer")
        self.user.connect_console(self)
        self.user.set_description('joe test', 'our test player named joe')
        self.user.set_max_weight_carried(750000)
        self.user.set_max_volume_carried(2000)
        self.verbose = False
        self.alias_map = {'n':  'north',
                          's':  'south',
                          'e':  'east', 
                          'w':  'west',  }

    def debug(self, x):
        if self.verbose:
            self.write(x)

    def write(self, text):
        print(text)

    def loop(self):
        while True:
            stop_going = self.parse()
            if stop_going:
                break

    def parse(self):
        self.last_text = input('-> ')  # store the most recent thing user typed
        if self.last_text == 'quit':
            return True
        if self.last_text == 'verbose':
            if self.verbose is False:
                self.verbose = True
                self.write("Verbose debug output now on.")
            else:
                self.verbose = False
                self.write("Verbose debug output now off.")
            return False
        self.words = self.last_text.split()
        if len(self.words) == 0:
            return False
        if self.words[0] == 'alias':
            if len(self.words) == 3:
                self.alias_map[self.words[1]] = self.words[2]
                self.write('new alias - %s is now an alias for %s' % (self.words[1], self.words[2]))
            else:
                self.write('to create a new alias, type "alias (new alias)"'
                           '(what the new alias should replace).'
                           ' please try again')
            return False
        # replace any aliases with their completed version
        for o in range(0, len(self.words)):
            t = self.words[o]
            if t in self.alias_map:
                self.words[o] = self.alias_map[t]
                self.debug("replacing alias %s with expansion %s" % (t, self.alias_map[t]))

        sV = self.words[0]   # verb as string
        sDO = None           # Direct object as string
        oDO = None           # Direct object as object
        sIDO = None          # Indirect object as string
        oIDO = None          # Indirect object as object

        num_words = len(self.words)
        a = 0
        while a < num_words:
            self.debug('parser: a is %d, self.words[a] is %s' % (a, self.words[a]))
            if self.words[a] in ['a', 'an', 'the']:
                self.debug('parser: %s is an article, so removing' % self.words[a])
                del self.words[a]
                num_words = num_words - 1
            a = a + 1

        if (len(self.words) > 1):
            sDO = self.words[1]
        ## TODO: code to remove articles, find prepositions & IDOs, etc
        
        
        possible_nouns = [self.user.location]           \
                       + [self.user]                    \
                       + self.user.contents             \
                       + self.user.location.contents

        for i in possible_nouns:
            self.debug("parser: possible_nouns includes %s " % (i.id))
            if i.id == sDO:
                self.debug("parser: found a match! setting oDO to %s" % (i.id))
                oDO = i
                break
            else:
                if sV in list(i.verb_dict):
                    self.debug("parser: doesn't match user-typed DO %s, but supports verb %s" % (sDO,sV))
                    if oDO == None:
                        self.debug("parser: setting oDO to %s" % (i.id)) 
                        oDO = i

        if oDO:
            verb = oDO.verb_dict[sV]
            self.debug("%s . verb_dict[%s]= %s" % (oDO.id, sV, verb))
        else:
            self.write('Sorry, could not find a noun matching %s for verb %s.' % (sDO, sV))
            return False
        
        # all verb functions take console, direct (or invoking) object, indirect object
        verb(self, oDO, oIDO)
        return False

cons = Console()

bedroom = Room('bedroom')
hallway = Room('hallway')
kitchen = Room('kitchen')
entryway = Room('entryway')
woods = Room('woods')

bedroom.set_description('a dusty bedroom', 'The bare board walls of this bedroom are dusty. A musty smell fills the air.')
hallway.set_description('a dusty hallway', 'This hallway has dusty walls made of wood. It is dim.')
kitchen.set_description('a dusty kitchen with 50-year old apliences and decorations', 'This kitchen looks about 50 years old, and is very dusty but apears still useable.')
entryway.set_description('a barren entryway', 'The dusty entryway has one chandelier hanging from the celing.')
woods.set_description('some bright and cheerful woods', 'Theese woods have happy birdsongs and pretty trees. They are bright.')

woods.add_exit('west', entryway)
entryway.add_exit('east', woods)
entryway.add_exit('southwest', kitchen)
entryway.add_exit('south', hallway)
hallway.add_exit('north', entryway)
hallway.add_exit('northwest', kitchen)
hallway.add_exit('southeast', bedroom)
bedroom.add_exit('northwest', hallway)
kitchen.add_exit('northeast', entryway)
kitchen.add_exit('southeast', hallway)

bed = Thing('bed')
bed.set_description('a queen-size bed', 'A plain and simple queen-size bed.')
bed.set_weight(150000)
bed.set_volume(6000)
bedroom.insert(bed)

bag = Container('bag')
bag.set_description('a normal bag', 'A normal-looking brown bag.')
bag.set_weight(100)
bag.set_volume(10)
bag.set_max_weight_carried(20000)
bag.set_max_volume_carried(10)
woods.insert(bag)

plate = Thing('plate')
plate.set_description('a dinner plate', 'This is a normal-looking white dinner plate.')
plate.set_weight(1000)
plate.set_volume(1.25)
kitchen.insert(plate)

woods.insert(cons.user)
cons.loop()
