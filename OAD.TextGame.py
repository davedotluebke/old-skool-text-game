class Thing:
    def __init__(self, ID):
        self.id = ID
        self.weight = 0.0
        self.volume = 0.0
        self.location = None
        self.short_desc = 'need_short_desc'
        self.long_desc = 'need_long_desc'
        # dictionary mapping verb strings to functions:
        self.verb_dict = {"look":           self.look_at,
                          }
        self.contents = None        # None - Containers can't contain things

    def set_weight(self, grams):
        if (grams < 0):
            cons.write("Error: weight cannot be negative")
            raise
        else:
            self.weight = grams

    def set_volume(self, liters):
        if (liters < 0):
            cons.write("Error: volume cannot be negative")
            raise
        else:
            self.volume = liters

    def set_location(self, containing_object):
        self.location = containing_object

    def set_description(self, s_desc, l_desc):
        self.short_desc = s_desc
        self.long_desc = l_desc

    def new_verb(self, verb, func):
        self.verb_dict[verb] = func

    def heartbeat(self):
        pass

    # # How likely that the user input text refers to this object
    # # 0.0 = No way!
    # # 0.5 = Maybe
    # # 1.0 = Definitely
    # def handle_user_input(self, sV, sDO):
    #     if sDO == i.id:
    #         return 1.0
    #     elif sV in list(self.verb_dict):
    #         return 0.5
    #     else:
    #         return 0

    def look_at(self, cons, oDO, oIDO):  # print out the long description of the thing
        cons.write(self.long_desc)

    def move_to(self, cons, oDO, oIDO):
        if self.location != None:
            self.location.extract(self)
            oDO.insert(self)


class Container(Thing):
    def __init__(self, ID):
        Thing.__init__(self, ID)
        self.contents = []
        self.max_weight_carried = 1
        self.max_volume_carried = 1

    def insert(self, obj):
        # error checking for max weight etc goes here
        contents_weight = 0
        contents_volume = 0
        for w in self.contents:
            contents_weight = contents_weight + w.weight
            contents_volume = contents_volume + w.volume
        if self.max_weight_carried >= contents_weight and self.max_volume_carried >= contents_volume:
            obj.set_location(self)   # make this container the location of obj
            self.contents.append(obj)
        else:
            cons.write("The weight(%d) and volume(%d) of the %s can't be held by the %s, "
                  "which can only carry %d grams and %d liters (currently "
                  "holding %d grams and %d liters)" 
                  % (obj.weight, obj.volume, obj.id, self.id, self.max_weight_carried, self.max_volume_carried, contents_weight, contents_volume))

    def set_max_weight_carried(self, max_grams_carried):
        self.max_weight_carried = max_grams_carried

    def set_max_volume_carried(self, max_liters_carried):
        self.max_volume_carried = max_liters_carried

# somelist = [x for x in somelist if not determine(x)]
    def extract(self, obj):
        if (obj in self.contents) == False:
            cons.write("Error! ",self.id," doesn't contain item ",obj.id)
            return
            
        found = -1
        for i in range(0, len(self.contents)):
            if obj == self.contents[i]:
                found = i
                break
        assert found != -1
        del self.contents[i]

    def look_at(self, cons, oDO, oIDO):
        Thing.look_at(self, cons, oDO, oIDO)
        if bool(len(self.contents)) and self.contents != [cons.user]:
            cons.write("Inside there is:")
            for item in self.contents:
                if item != cons.user:
                    cons.write(item.short_desc)
        else:
            cons.write("It is empty.")


class Room(Container):
    def __init__(self, ID):
        Container.__init__(self, ID)
        self.exits = {}
        self.set_max_weight_carried(4e9)
        self.set_max_volume_carried(3e9)
        self.verb_dict["go"]        = self.go_to
        self.verb_dict["walk"]      = self.go_to

    def add_exit(self, exit_name, exit_room):
        self.exits[exit_name] = exit_room

    def look_at(self, cons, oDO, oIDO):
        Container.look_at(self, cons, oDO, oIDO)
        cons.write('exits are:')
        for e in self.exits:
            cons.write(e)

    def move_to(self, cons, oDO, oIDO):
        cons.write('rooms cannot be moved into %s!' % oIDO.id)

    def go_to(self, cons, oDO, oIDO):
        words = cons.words
        cons.debug("verb function go_to: words == ")
        cons.debug(words)
        sExit = words[1]
        if sExit in list(self.exits):
            dest = self.exits[sExit]
            cons.write("You %s to the %s into the %s." % (words[0], sExit, dest.id))
            cons.user.move_to(cons, dest, None)
            cons.write("You enter %s." % cons.user.location.short_desc)
            cons.write("exits are:")
            for w in cons.user.location.exits:
                cons.write(w)


class Creature(Container):
    def __init__(self, ID):
        Container.__init__(self, ID)
        self.hitpoints = 10     # default hitpoints
        self.health = self.hitpoints  # default full health (0 health --> dead)


class Player(Creature):
    def __init__(self,ID):
        Creature.__init__(self, ID)
        self.cons = None

    def connect_console(self, c):
        self.cons = c

class Console:
    def __init__(self):
        self.user = Player("testplayer")
        self.user.connect_console(self)
        self.user.set_description('joe test', 'our test player named joe')
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
        self.last_text = input('> ')  # store the most recent thing user typed
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
    
woods.insert(cons.user)
cons.loop()
