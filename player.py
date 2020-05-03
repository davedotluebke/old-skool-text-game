import pickle
import sys
import importlib
import connections_websock
import os
import logging

import gametools

from thing import Thing
from room import Room
from creature import Creature
from action import Action
from conshandler import ConsHandler


def clone(params=None):
    if params:
        ID = params[0]
        console = params[1]
    else:
        ID = ""
        console = None
    player = Player(ID, __file__, console)
    return player

# convention: tuple of (intransitive_self, intransitive_others, transitive_self, transitive_others, transitive_target)
emotes = {'bow':    ('You take a sweeping bow.', 
                    '&nD%s takes a sweeping bow.', 
                    'You bow to &nd%s.', 
                    '&nD%s bows to &nd%s.', 
                    '&nD%s bows to you.'),
          'giggle': ('You giggle.', 
                    '&nD%s giggles.', 
                    'You giggle at &nd%s.', 
                    '&nD%s giggles at &nd%s.',
                    '&nD%s giggles at you.')
         }

class Player(Creature):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, ID, path, console):
        """Initialize the Player object and attach a console"""
        Creature.__init__(self, ID, path)
        self.cons = console
        self.login_state = None
        self.password = None
        self.start_loc_id = None
        self.handlers = {}  # list of debug handlers for wizards
        self.set_description("formless soul", "A formless player without a name")
        self.set_weight(175/2.2)
        self.set_volume(66)
        self.set_max_weight_carried(750000)
        self.set_max_volume_carried(2000)
        self.saved_cons_attributes = []
        self.aggressive = 1         #TODO: Specialized individual stats
        self.armor_class = 10
        self.combat_skill = 40
        self.strength = 20
        self.dexterity = 60
        self.attack_now = 0
        self.auto_attack = True
        self.engaged = False
        self.wizardry_skill = 0
        self.wizardry_element = None
        self.wprivileges = False
        self.attacking = False
        self.hitpoints = 20
        self.health = 20
        self.species = None
        self.gender = None
        self.adj1 = None
        self.adj2 = None
        self.terse = False  # True -> show short description when entering room
        self.game.register_heartbeat(self)
        self.versions[gametools.findGamePath(__file__)] = 2
        self.prev_location_id = None
        self.tutorial_messages = {
            'domains.character_creation.species': 'Try typing "look north mirror" and then "enter north mirror".',
            'domains.character_creation.adjective1': 'Try intoning something from the plaque.',
            'domains.school.school.great_hall': 'Try going to the east.'
        }
        self.tutorial_act_messages = {
            'look': 'Now try entering one of the mirrors.'
        }
        self.tutorial_act_messages_complete = {
            'look': False
        }
        
    def get_saveable(self):
        saveable = super().get_saveable()
        try:
            del saveable['enemies']
        except KeyError: 
            pass
        del saveable['cons']
        return saveable

    def update_cons_attributes(self):
        try:
            self.cons.alias_map = self.saved_cons_attributes[0]
            self.cons.measurement_system = self.saved_cons_attributes[1]
        except (AttributeError, IndexError) as e:
            pass

    def save_cons_attributes(self):
        self.saved_cons_attributes = [self.cons.alias_map, self.cons.measurement_system]
    
    def update_version(self):
        if hasattr(self, 'version_number'):
            self.versions[gametools.findGamePath(__file__)] = 1
        
        super().update_version()

        if self.versions[gametools.findGamePath(__file__)] == 1:
            self.password = "{\"F\":[1779033703,-1150833019,1013904242,-1521486534,1359893119,-1694144372,528734635,1541459225],\"A\":[1634952294],\"l\":32}"
            self.versions[gametools.findGamePath(__file__)] = 2
        if self.versions[gametools.findGamePath(__file__)] == 2:
            if hasattr(self, "wprivilages"):
                self.wprivileges = self.wprivilages
                del self.wprivilages
            self.versions[gametools.findGamePath(__file__)] = 3

    #
    # INTERNAL USE METHODS (i.e. _method(), not imported)
    #
    def _restore_objs_from_IDs(self):
        super()._restore_objs_from_IDs()
        if isinstance(self.adjectives, list):
            self.adjectives = set(self.adjectives)

    def _handle_login(self, cmd):
        state = self.login_state
        if state == 'AWAITING_USERNAME':
            if  len(cmd.split()) != 1:
                self.cons.write("Usernames must be a single word with no spaces.\n"
                                "Please enter your username:")
                return
            self.names[0] = cmd.split()[0]  # strips any trailing whitespace
            filename = gametools.realDir(gametools.PLAYER_DIR, self.names[0]) + '.OADplayer'
            try:
                f = open(filename, 'r+b')
                f.close()  # success, player exists, so close file for now & check password
                self.cons.write("Welcome back, %s!\nPlease enter your --#password: " % self.names[0])
                self.login_state = 'AWAITING_PASSWORD'
            except FileNotFoundError:
                self.cons.write("No player named "+self.names[0]+" found. "
                            "Would you like to create a new player? (yes/no)\n")
                self.login_state = 'AWAITING_CREATE_CONFIRM'
            return
        elif state == 'AWAITING_CREATE_CONFIRM':
            if cmd == "yes": 
                self.cons.write("Welcome, %s!\nPlease create a --#password:" % self.names[0])
                self.login_state = 'AWAITING_NEW_PASSWORD'
                return
            elif cmd == "no":
                self.cons.write("Okay, please enter your username: ")
                self.login_state = 'AWAITING_USERNAME'
                return
            else:
                self.cons.write("Please answer yes or no: ")
                return
        elif state == 'AWAITING_NEW_PASSWORD':
            passwd = cmd
            # XXX temporary fix for now
            self.password = passwd
            # TODO secure password authentication goes here
            self.id = self._add_ID(self.names[0])            
            self.proper_name = self.names[0].capitalize()
            self.log.info("Creating player id %s with default name %s" % (self.id, self.names[0]))
            start_room = gametools.load_room(gametools.NEW_PLAYER_START_LOC)
            start_room.insert(self)
            self.perceive("\nWelcome to Firefile Sorcery School!\n\n"
            "Type 'look' to examine your surroundings or an object, "
            "'inventory' to see what you are carrying, " 
            "'quit' to end the game, and 'help' for more information.")
            self.login_state = None
            return
        elif state == 'AWAITING_PASSWORD':
            passwd = cmd
            # XXX temporary fix, need more security
            # TODO more secure password authentication goes here
            for oid in Thing.ID_dict:
                if isinstance(Thing.ID_dict[oid], Player) and Thing.ID_dict[oid].names[0] == self.names[0] and passwd == Thing.ID_dict[oid].password:
                    self.cons.write("A copy of %s is already in the game. Would you like to take over %s? (yes/no)" % (self.names[0], self.names[0]))
                    self.login_state = 'AWAITING_RECONNECT_CONFIRM'
                    return
            filename = gametools.realDir(gametools.PLAYER_DIR, self.names[0]) + '.OADplayer'
            try:
                try:
                    newuser = self.game.load_player(filename, self.cons, password=passwd)
                    self.log.info("Loaded player id %s with default name %s" % (newuser.id, newuser.names[0]))
                    newuser.login_state = None
                    self.login_state = None
                    self.game.deregister_heartbeat(self)
                    del Thing.ID_dict[self.id]
                except gametools.IncorrectPasswordError:
                    self.cons.write("Your username or password is incorrect. Please try again.")
                    self.login_state = "AWAITING_USERNAME"
            except gametools.PlayerLoadError:
                self.cons.write("Error loading data for player %s from file %s. \n"
                                "Please try again.\nPlease enter your username: " % (self.names[0], filename))
                self.login_state = "AWAITING_USERNAME"
        elif state == 'AWAITING_RECONNECT_CONFIRM':
            if cmd == 'yes':
                for oid in Thing.ID_dict:
                    if isinstance(Thing.ID_dict[oid], Player) and Thing.ID_dict[oid].names[0] == self.names[0]:
                        break
                for websocket in connections_websock.conn_to_client:
                    if connections_websock.conn_to_client[websocket] == self.cons:
                        connections_websock.conn_to_client[websocket] = Thing.ID_dict[oid].cons
                        Thing.ID_dict[oid].cons.connection = websocket
            elif cmd == 'no':
                self.cons.write("Okay, please enter your username: ")
                self.login_state = "AWAITING_USERNAME"
                return
            elif cmd == 'restart':
                self.cons.write("Erasing existing character and restarting from last save. Please enter your --#password again.")
                for oid in Thing.ID_dict:
                    if isinstance(Thing.ID_dict[oid], Player) and Thing.ID_dict[oid].names[0] == self.names[0]:
                        break
                self.game.deregister_heartbeat(Thing.ID_dict[oid])
                del Thing.ID_dict[oid]
                self.login_state = "AWAITING_PASSWORD"
            else:
                self.cons.write("Please answer yes or no: ")
                return
    
    def _schedule_interactive_tutorial(self, act):
        if self.prev_location_id != self.location.id:
            if self.location.id in self.tutorial_messages:    # list of rooms with interactive tutorial messages
                Thing.game.schedule_event(30, self.provide_interactive_tutorial, self.location.id)
        if act in self.tutorial_act_messages and not self.tutorial_act_messages_complete[act]:
            Thing.game.schedule_event(15, self.provide_interactive_tutorial, act)
        self.prev_location_id = self.location.id
    
    def provide_interactive_tutorial(self, rid_act):
        if rid_act in self.tutorial_messages:
            self.cons.write(self.tutorial_messages[rid_act])
        
        if rid_act in self.tutorial_act_messages:
            self.cons.write(self.tutorial_act_messages[rid_act])
            self.tutorial_act_messages_complete[rid_act] = True
    #
    # SET/GET METHODS (methods to set or query attributes)
    #
    def set_start_loc(self, startroom):
        self.start_loc_id = startroom.id

    def get_saveable(self):
        saveable = super().get_saveable()
        try:
            del saveable['enemies']
        except KeyError: 
            pass
        del saveable['cons']
        return saveable

    #
    # OTHER EXTERNAL METHODS (misc externally visible methods)
    #
    def detach(self, nocons=False):
        # TODO: Deal with logs in player
        if not nocons:
            self.cons.detach(self)
        self.cons = None
        self.destroy()
        
    def heartbeat(self):
        if self.cons == None:
            self.detach(nocons=True)
        
        if self.health < self.hitpoints:
            self.heal()
        
        cmd = self.cons.take_input()
        if self.login_state != None:
            if cmd != None and cmd != '__noparse__' and cmd != '__quit__':
                self._handle_login(cmd)
            return
        sV = None
        if cmd:
            if cmd != '__noparse__' and cmd != '__quit__':
                sV = Thing.game.parser.parse(self, self.cons, cmd)
            elif cmd == '__quit__':
                self.detach()
        
        if sV:
            self._schedule_interactive_tutorial(sV)

        if self.auto_attack:            # TODO: Player Preferences
            if self.attacking:
                if self.attacking == 'quit':
                    return
                else:
                    self.attack_enemy(self.attacking)
                    return
            try:
                for i in self.location.contents:
                    if i in self.enemies:
                        self.cons.write('You attack your enemy %s.' % i._short_desc)
                        self.attacking = i
                        self.attack_enemy(i)
            except AttributeError:
                self.log.error('Error! Location is a string!')
        elif self.engaged:
            if self.attacking:
                if self.attacking == 'quit':
                    return
                else:
                    self.attack_enemy(self.attacking)
                    return

    def die(self, message):
        Creature.die(self, message)
        self.cons.write("You have died!\n\nFortunately you are reincarnated immediately...")
        self.health = self.hitpoints
        if (self.start_loc_id):
            room = Thing.ID_dict[self.start_loc_id]
            self.move_to(room)
            room.report_arrival(self)
        else:
            self.cons.write("Uh-oh! You don't have a starting location. You are in a great void...")

    def perceive(self, message, silent=False, force=False):
        '''Parse a string passed to `emit()` and customize it for this
        player. Searches the string for special tags (indicated with the '&'
        symbol) and replaces the substring following that tag (up to a 
        whitespace character) with a customized substring. Currently supports
        the following tags, in which <id> is the ID attribute of an object O:

            tag      description
            -------  --------------------------------------------------------
            &nd<id>: 'name-definite': replace with the proper name of O, if O
                     has been introduced to this player, else the short
                     description of O preceeded by the definite article 'the'
            &nD<id>: 'name-capitalized-definite': replace with the proper name
                     of O, if O has been introduced to this player, else the
                     short description of O proceeded by the capitalized 
                     definite article 'The'
            &ni<id>: 'name-indefinite': replace with O.proper_name if O has 
                     been introduced, else O._short_desc preceeded by the 
                     indefinite article ('a' or 'an')
            &nI<id>: 'name-indefinite-capitalized': replace with O.proper_name
                     if O has been introduced, else 'A' or 'An' + O._short_desc
            &nn<id>: 'name-no-article': replace with O.proper_name if O has 
                     been introduced, else O._short_desc with no article.

            &s<id>:  'species': replace with species name (`O.species`)
            &S<id>:  'species-capitalized': replace with capitalized species
                     name (`O.species.upper()`)

            &p<id>:  'pronoun': replace with 'he', 'she', or 'it'
            &P<id>:  'pronoun-capitalized': replace with 'He', 'She', or 'It'

            &v<id>:  'possessive': replace with 'his', 'her', or 'its'
            &V<id>:  'possessive-capitalized': replace with 'His', 'Her', 'Its'      

            &u:      'user-id': replace with the user id of the perceiver, to
                     be used as the <id> part of the above tags.
        
        In general, a creature mentioned 'by name' in the message probably will 
        get a custom message and shouldn't get the default 'perceive' message.  
        So for convenience `perceive()` will silently return if this player is
        one of the creatures named using the &n semantics above, effectively 
        ignoring any creatures named in the `emit()` message.

        If the <silent> flag is set, do not actually write the constructed message
        to the player's console, but instead return it as a string.

        If the [force] flag is set, make the player print the message even if the 
        room is dark.
        '''
        if not self.location.is_dark() or force:
            # replace any & tags in the message 
            while True:
                # first, replace any occurrence of '&u' with the user's ID
                (m1, sep, m2) = message.partition('&u')  
                if not sep:    # partition() sets sep to '' if '&u' not found
                    break
                message = m1 + self.id + m2
            while True:
                (m1, sep, m2) = message.partition('&')  
                if not sep:    # partition() sets sep to '' if '&' not found
                    break
                tag = m2.split()[0]  # split() separates on whitespace
                subject = ""
                O = None
                try:
                    tag_type = tag[0:1]
                    idstr = tag[1:]
                    if tag_type in ('n', 'N'):  # some tag types use 2 letters
                        tag_type = tag[0:2]
                        idstr = tag[2:]
                    idstr = idstr.rstrip('.,!?;:\'"')  # remove any punctuation
                    O = Thing.ID_dict[idstr]
                except IndexError:
                    subject = "<error: can't parse tag &%s>" % tag
                except KeyError:
                    subject = "<error: can't find object %s>" % idstr
                if tag_type[0] == 'n':
                    if O == None:
                        subject = '[Error: no object matching idstr %s]' % idstr
                    elif O == self: 
                        return      # ignore messages that mention self by name
                    else:
                        subject = O.get_short_desc(self)
                        if tag_type[1] in ('d','D'):
                            subject = O.get_short_desc(self, definite=True)
                        if tag_type[1] in ('i','I'):
                            subject = O.get_short_desc(self, indefinite=True)
                        if tag_type[1] in ('N','D','I', 'R'):
                            subject = subject.capitalize()
                if tag_type[0] == 's':
                    subject = O.species
                if tag_type[0] == 'S':
                    subject = O.species.capitalize()
                if tag_type[0] == 'p':
                    subject = O.pronoun()
                if tag_type[0] == 'P':
                    subject = O.pronoun().capitalize()
                if tag_type[0] == 'v': 
                    subject = O.possessive()
                if tag_type[0] == 'V':
                    subject = O.possessive().capitalize()
                
                m2 = subject + m2.partition(tag)[2]
                message = m1 + m2

            super().perceive(message)
            if silent:
                return message
            else:
                self.cons.write(message) 
                   
    def attack_enemy(self, enemy):
        if self.attacking in self.location.contents:
            self.attack(enemy)
        else:
            self.attacking = None

    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    #
    # Wizard-specific actions:
    #   
    def execute(self, p, cons, oDO, oIDO):
        if cons.user != self:
            return "I don't quite get what you mean."
        if not self.game.is_wizard(self.name()):
            return "You cannot yet perform this magical incantation correctly."
        cmd = ' '.join(p.words[1:])
        cons.write("Executing command: `'%s'`" % cmd)
        try: 
            exec(cmd)
        except Exception as inst:
            cons.write("Unexpected error: `" + str(sys.exc_info()[0]) + "\n\t" + str(sys.exc_info()[1])+"`")
            # cons.write(type(inst)+"\n"+inst)    # the exception instance
        return True

    def fetch(self, p, cons, oDO, oIDO):
        '''Find an in-game object by ID and bring it to the player.'''
        if cons.user != self:
            return "I don't quite get what you mean."
        if not self.game.is_wizard(self.name()):
            return "You cannot yet perform this magical incantation correctly."
        if len(p.words) < 2: 
            cons.write("Usage: 'fetch <id>', where id is an entry in `Thing.ID_dict[]`")
            return True
        id = " ".join(p.words[1:])
        try:
            obj = Thing.ID_dict[id]
            if isinstance(obj, Creature) or obj.move_to(self) == False:
                if obj.move_to(self.location) == False:
                    cons.write("You attempt to fetch the %s but somehow cannot bring it to this place." % obj.names[0])
                else:
                    cons.write("You perform a magical incantation and bring the %s to this place!" % obj.names[0])
            else:
                cons.write("You perform a magical incantation and the %s appears in your hands!" % obj.names[0])
            self.emit("&nD%s performs a magical incantation, and you sense something has changed." % self.id, [self])
        except KeyError: 
            return "There seems to be no object with true name '%s'!" % id
        
        return True                    

    def clone(self, p, cons, oDO, oIDO):
        '''Clone a new copy of an object specified by ID or by module path, and bring it to the player.'''
        if cons.user != self:
            return "I don't quite get what you mean."
        if not self.game.is_wizard(self.name()):
            return "You cannot yet perform this magical incantation correctly."
        if len(p.words) < 2: 
            cons.write("```"
                       "Usage:\n\t'clone <id>', where id is an entry in Thing.ID_dict[]"
                       "\n\t'clone <path>', where path is of the form 'domains.school.test_object'"
                       "```")
            return True
        id = " ".join(p.words[1:])
        try:
            current_obj = Thing.ID_dict[id]
            objpath = current_obj.path
        except KeyError: 
            objpath = id
        obj = gametools.clone(objpath)
        if obj == None:
            return "There seems to be no object with true name `'%s'`!" % id
        if isinstance(obj, Creature) or obj.move_to(self) == False:
            if obj.move_to(self.location) == False:
                cons.write("You attempt to clone the %s but somehow cannot bring it to this place." % obj.names[0])
            else:
                cons.write("You perform a magical incantation and bring the %s to this place!" % obj.names[0])
        else:
            cons.write("You perform a magical incantation and the %s appears in your hands!" % obj.names[0])
        self.emit("&nD%s performs a magical incantation. You sense something has changed." % self.id, [self])
        
        return True                    

    def debug(self, p, cons, oDO, oIDO):
        '''Start or stop debug logging for player actions, for a module, or for an object in the game.'''
        usage = """Usage: `debug [sec] [level] obj`
        The `obj` argument may be:
        - a visible object or creature
        - an object id (i.e. an entry in `Thing.ID_dict[]`)
        - a path of the form `domains.school.example_object`
        - the keyword `here`, which specifies the room containing the player
        - the keyword `me`, which specifies the player object itself.
        The optional `[sec]` argument specifies the duration, in seconds, of the debug logging. The default is 60 seconds.
        The optional `[level]` argument must be one of `debug`, `info`, `warning`, or `error`. All log messages at the specified level are displayed. If left unspecified, `[level]` defaults to `debug`.
        """
        DEFAULT_DEBUG_DURATION = 60
        DEFAULT_DEBUG_LEVEL = 'debug'
        if cons.user != self:
            self.log.error("`player.debug()` action called but cons.user is %s instead of self!" % cons.user)
            return "I don't quite get what you mean."
        if not self.game.is_wizard(self.name()):
            return "You cannot yet perform this magical incantation correctly."
        if len(p.words) < 2: 
            return usage
        # find & strip the seconds operator and debug level, if specified
        sec = [s for s in p.words[1:] if s.isnumeric()]
        sec = sec[0] if sec else DEFAULT_DEBUG_DURATION 
        levels = {'critical', 'error', 'warning', 'info', 'debug'}
        dbg_level = [d for d in p.words[1:] if d in levels]
        dbg_level = dbg_level[0] if dbg_level else DEFAULT_DEBUG_LEVEL
        dbg_level = dbg_level.upper()
        w = p.words[:1] + [x for x in p.words[1:] if not x.isnumeric() and x not in levels]
        if oDO:
            obj = oDO # player specified an object that the parser understands
        else:
            if w[1] == "me":
                obj = self
            elif w[1] == "here":
                obj = self.location
            else: 
                # re-parse the stripped words[] to find possible objects
                # TODO: encapsulate this code from parse() rather than cut-and-pasting it
                oDO_list = []
                (sV, sDO, sPrep, sIDO) = p.diagram_sentence(w)
                # FIRST, search for nearby objects that support the verb user typed
                possible_objects = p._collect_possible_objects(self, inventory=True, environment=True)
                # THEN, check for objects matching the direct & indirect object strings
                if sIDO:  
                    return usage  # debug command accepts exactly 1 direct object
                if sDO:   
                    # set oDO to object(s) matching direct object strings
                    oDO_list = p.find_matching_objects(sDO, possible_objects, cons)
                if not sDO or not oDO_list:
                    return "ERROR: No object specified to debug!\n\n" + usage
                if len(oDO_list) > 1:
                    return "ERROR: Multiple objects specified to debug!\n\n" + usage
                obj = oDO_list[0]
        # Check if this player already has a handler for this object
        if obj.id in self.handlers:
            self.remove_dbg_handler(obj)
            return True
        self.perceive(f"Now debugging object `{obj.id}` at level `{dbg_level}` for the next {sec} seconds!")
        dbg_handler = ConsHandler(cons, dbg_level)
        obj.log.addHandler(dbg_handler)
        self.handlers[obj.id] = dbg_handler
        # Add an event to remove & destroy dbg_handler in <duration> seconds
        self.cons.game.schedule_event(int(sec), self.remove_dbg_handler, obj)
        return True

    def remove_dbg_handler(self, obj):
        try: 
            handler = self.handlers[obj.id]
        except AttributeError or KeyError:
            self.log.error(f"remove_debug_handler() called for `{obj}` but no handler stored for player `{self.id}`!")
            return
        try: 
            obj.log.removeHandler(handler)
            handler.close()
            del self.handlers[obj.id]
            self.perceive(f"No longer debugging object `{obj}`.")
        except AttributeError:
            self.log.error(f"AttributeError removing debug handler {handler} from object {obj}")


    def reload_room(self, p, cons, oDO, oIDO):
        '''Reloads the specified object, or the room containing the player if none is given.
        First extracts all of the objects from the room, then re-imports the object 
        module, calls `load()` or `clone()` in the new module, then finally moves any creatures including
        players back to the new room.'''
        obj = None
        if not self.game.is_wizard(self.name()):
            return "You cannot yet perform this magical incantation correctly."
        if isinstance(obj, Creature):
            return "You cannot reload players or NPCs!"
        if len(p.words) < 2: 
            obj = self.location
        elif len(p.words) == 2:
            obj = gametools.load_room(p.words[1])
            if obj == None:
                obj = gametools.clone(p.words[1])
                if obj == None:
                    return "Error, room or object '%s' doesn't seem to exist!" % p.words[1]
        else: 
            return "Usage: 'reload' [object path]\n\t[object path\ is optional, if none is given will reload the current room."

        if obj.contents != None:
            alive = [x for x in obj.contents if isinstance(x, Creature)] # all Creatures incl NPCs & players (usefull if room)
            if obj.detach(obj.path) == False:
                return "Error while detaching object %s!" % obj.path
        else:
            alive = []
        mod = importlib.reload(obj.mod)
        try:
            if isinstance(obj, Room):
                if obj.params:
                    newobj = mod.load(obj.params)
                else:
                    newobj = mod.load()  # TODO: store and re-use parameters of original load() call?
        except Exception:
            self.log.error('Error reloading object %s!' % obj)
            cons.user.perceive('An error occured while reloading %s.' % obj)
            for c in alive:
                c.move_to(obj)
            return True
        if isinstance(obj, Room):
            for c in alive: 
                c.move_to(newobj, force_move = True)
        else:
            thing_id_list = list(Thing.ID_dict)
            for cidx in thing_id_list:
                c = Thing.ID_dict[cidx]
                if c.path == obj.path and obj is not c:
                    new_c = gametools.clone(obj.path)
                    if c.location:
                        new_c.move_to(c.location, merge_pluralities=False)
                    c.destroy()
        cons.write('You make a magical gesture and scene around you suddenly changes.')
        self.emit('&nD%s makes a magical gesture, and you sense something has changed.' % self.id)
        obj.destroy()
        return True

    def apparate(self, p, cons, oDO, oIDO):
        """Teleport the wizard to a given room, specified by id or path."""
        if cons.user != self:
            return "I don't quite get what you mean."
        if not self.game.is_wizard(self.name()):
            return "You cannot yet perform this magical incantation correctly."
        if len(p.words) < 2: 
            cons.write("Usage: 'apparate <id>', where id is the entry of a Room in `Thing.ID_dict[]` or a path to its module")
            return True
        id = " ".join(p.words[1:])
        try:
            room = Thing.ID_dict[id]
        except KeyError: 
            room = gametools.load_room(id)
        if room == None:
            return "There seems to be no place with id (or path) '%s'!" % id
        if isinstance(room, Room) == False:
                cons.write("You cannot apparate to %s; that is not a place!" % room.names[0])
                return True
        self.emit("&nD%s performs a magical incantation, and vanishes!" % self.id, [self])
        self.move_to(room)
        self.emit("&nD%s arrives suddenly, as if by magic!" % self.id, [self])
        self.perceive("You perform a magical incantation and are suddenly in a new place!")
        room.report_arrival(self, silent=True)
        return True

    def groups(self, p, cons, oDO, oIDO): 
        """Change or list player-group associations, e.g. add player to 'wizards' or 'admins' group."""
        usage = "**Usage**: groups [add|remove|create] [player] [group]\n"\
        "  Adds or removes the specified player to/from the specified group, or lists the "\
        "player-group associations for the specified player and/or group. Both player "\
        "and group must be given if an action (add/remove/create) is specified.  If both "\
        "player and group are specified but no action (add/remove/create), the player is added or "\
        "removed from the group depending on whether the player already belonged to the group. "\
        "If create is specified, it will create the group if the player does not exist. " \
        "The special player string 'me' can be used to indicate the calling user.  "
        
        if cons.user != self:
            return "I don't quite get what you mean."  
        if not self.game.is_wizard(self.name()):
            return "You cannot yet perform this magical incantation correctly."  
        words = p.words    
        if len(words) < 2:
            cons.write(usage + '\n' + cons.game.list_wizard_roles())
            return True
        if words[1] == 'add' or words[1] == 'remove' or words[1] == 'create':
            # next arguments should be <player> <group>
            if len(words) != 4:
                cons.write(usage)
                return True
            action, player, group = words[1], words[2], words[3]
        else:  # arguments might be <player>, or <group>, or <player> <group>
            if len(words) == 2:  # one argument, either <player> or <group>
                role_exists = words[1] in cons.game.roles
                if role_exists:  # argument is <group>
                    cons.write(cons.game.list_wizard_roles(role=words[1]))
                player = self.name() if words[1] == 'me' else words[1]
                player_exists = gametools.check_player_exists(player)
                if player_exists:  # argument is <player> 
                    cons.write(cons.game.list_wizard_roles(wiz=player))
                if not player_exists and not role_exists:
                    cons.write("Error: %s does not appear to be the name of a player or a group!" % words[1])
                return True
            if len(words) == 3:
                action, player, group = "toggle", words[1], words[2]
        player = self.name() if player == 'me' else player
        if not gametools.check_player_exists(player):
            cons.write("Error: no player named %s appears to exist!" % player)
            return True
        if not group in cons.game.roles and action != "create":
            cons.write("Error: no group named %s appears to exist!" % group)
            return True
        if action == "add" or action == "create" or (action == "toggle" and player not in cons.game.roles[group]): 
            cons.game.add_wizard_role(player, group)
            cons.write("Added %s to group %s" %(player, group))
        elif action == "remove" or (action == "toggle" and player in cons.game.roles[group]):
            cons.game.remove_wizard_role(player, group)
            cons.write("Removed %s from group %s" % (player, group))
        else:
            cons.write("Error: couldn't apply action %s to player %s and group %s!" % (action, player, group))
        return True        
        
            
        
    #
    # Non-wizard player actions:
    # 
    def inventory(self, p, cons, oDO, oIDO):
        if cons.user != self:
            return "You can't look at another player's inventory!"
        message = "You are carrying:\n"
        if not self.contents:
            message += '\tnothing'
        for i in self.contents:
            if i == self.weapon_wielding or i == self.armor_worn: 
                continue
            message += "\t&ni%s\n" % i.id
        if self.weapon_wielding != self.default_weapon: 
            message += 'You are wielding &nd%s.\n' % self.weapon_wielding.id
        if self.armor_worn != self.default_armor:
            message += 'You are wearing &nd%s.\n' % self.armor_worn.id
        self.perceive(message, force=True)
        return True
    
    def toggle_terse(self, p, cons, oDO, oIDO):
        if cons.user != self:
            return "I don't quite get what you mean."
        try: 
            if p.words[1] == "on": 
                self.terse = True
            elif p.words[1] == "off": 
                self.terse = False
            else: 
                return """Usage: 'terse [on/off]'
                Use long descriptions (off) or short descriptions (on) when entering a place.
                With no specifier, 'terse' toggles between on and off."""
        except IndexError:
            self.terse = not self.terse
        cons.write("Terse mode %s. %s" % ("on" if self.terse else "off",
            "Short descriptions will be used when entering a place; type 'look' for full description" if self.terse else
            "Full descriptions will be used entering a place."))
        # TODO: a mode that prints long description only when first entering a room
        return True
  
    def say(self, p, cons, oDO, oIDO):
        if cons.user != self:
            return "I don't quite get what you are trying to say."
        if len(p.words) < 2:
            return "What do you want to say?"
        self.emit("&nD%s %ss: %s" % (self.id, p.words[0], " ".join(p.words[1:])), ignore = [self])
        cons.write("You %s: %s" % (p.words[0], " ".join(p.words[1:])))
        return True
    
    def emote_action(self, p, cons, oDO, oIDO):
        if cons.user != self: 
            return "I don't quite get what you are trying to do."
        cmd = p.words[0]
        if cmd not in emotes:
            return "I don't quite understand what you are trying to do."
        if not oDO:
            # intransitive version of the emote verb
            self.perceive(emotes[cmd][0])
            self.emit(emotes[cmd][1] % self.id, [self])
        else:
            self.perceive(emotes[cmd][2] % oDO.id)
            self.emit(emotes[cmd][3] % (self.id, oDO.id), [self])
            if isinstance(oDO, Player):
                oDO.perceive(emotes[cmd][4] % self.id)     
        return True        
    
    def introduce(self, p, cons, oDO, oIDO):
        if cons.user != self:
            return "I'm not sure who's introducing whom."
        if len(p.words) < 2:
            return "Usage: 'introduce myself' or 'introduce <name>' with <name> of somebody present."
        if p.words[1] != 'myself':
            return "Introducing anybody other than 'myself' is not yet supported."
        self.emit("&nD%s introduces %s as '%s'." % (self.id, "themselves", self.proper_name))
        self.perceive("You introduce yourself to all.")
        for obj in self.location.contents:
            if isinstance(obj, Creature) and obj != self:
                try:
                    obj.introduced.add(self.id)
                except AttributeError: # XXX fix set save/restore code instead of this hack
                    obj.introduced = set(obj.introduced)
                    obj.introduced.add(self.id)
        return True

    def engage(self, p, cons, oDO, oIDO):
        if cons.user != self:
            return "I don't quite get what you mean."
        if not oDO:
            return "Who do you intend to engage in combat?"
        if not isinstance(oDO, Creature):
            return "You can't attack non-creatures!"
        self.attacking = oDO
        self.weapon_and_armor_grab()
        self.engaged = True
        self.perceive('You begin attacking &nd%s' % oDO)
        return True

    def disengage(self, p, cons, oDO, oIDO):        #TODO: Finish up.
        if cons.user != self:
            return "I don't quite get what you mean."
        self.attacking = 'quit'
        self.engaged = False
        return True

    actions = dict(Creature.actions)  # make a copy
    # Wizard-specific actions
    actions['execute'] =    Action(execute, True, True)
    actions['fetch'] =      Action(fetch, True, True)
    actions['clone'] =      Action(clone, True, True)
    actions['debug'] =      Action(debug, True, True)
    actions['apparate'] =   Action(apparate, True, True)
    actions['reload'] =     Action(reload_room, True, True)
    actions['groups'] =      Action(groups, True, True)
    # player actions
    actions['inventory'] =  Action(inventory, False, True)
    actions['terse'] =      Action(toggle_terse, False, True)
    actions['say'] =        Action(say, True, True)
    actions['shout'] =      Action(say, True, True)
    actions['mutter'] =     Action(say, True, True)
    actions['whisper'] =    Action(say, True, True)
    for verb in emotes:
        actions[verb] =     Action(emote_action, True, True)
    actions['introduce'] =  Action(introduce, True, True)
    actions['engage'] =  Action(engage, True, False)
    actions['attack'] =  Action(engage, True, False)
    actions['disengage'] =  Action(disengage, False, True)
