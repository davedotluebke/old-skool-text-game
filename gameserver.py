import io
import traceback
import random
import time
import asyncio
import socketserver
import http.server
import websockets
import connections_websock
import json

import gametools

from debug import dbg
from thing import Thing
from player import Player
from parse import Parser
from console import Console
from event_nsl import EventQueue
from parse import Parser
from server_key_detect import KBHit

class Game():
    """
        The Game class contains a parser, a list of players, a time counter, 
        a list of objects that have a heartbeat (a function that runs 
        periodically). It should also probably house the Twisted event loop 
        and associated factory for creating protocols (connections to clients)
    """
    def __init__(self):
        Thing.game = self  # only one game instance ever exists, so no danger of overwriting this
        self.handle_exceptions = True # game will catch all exceptions rather than let debugger handle them
        
        self.heartbeat_users = []  # objects to call "heartbeat" callback every beat
        self.time = 0  # number of heartbeats since game began
        self.events = EventQueue()  # events to occur in future 

        self.parser = Parser()
        self.dbg = dbg
        self.users = []

        self.ip_address = "127.0.0.1"
        self.runtime = 1
        self.run_timings = False
        self.last_seconds = time.time()

        self.kb = KBHit()
        self.current_input_str = ''
        self.current_prompt = '> '
        self.commands = {
            'quit':self.quit_game,
            'q':self.quit_game,
            'help':self.print_help_msg,
            'h':self.print_help_msg,
            'verbose':self.set_dbg_verbosity,
            'v':self.set_dbg_verbosity
        }

    def save_game(self, filename):
        raise NotImplementedError("Saving games no longer works.")
        if not filename.endswith('.OAD'): 
            filename += '.OAD'
        try:
            f = open(filename, 'w+b')
            # explicitly dump ID_dict to guarantee we dump all objects
            save = Thing.ID_dict, self
            pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
            self.cons.write("Saved entire game to file %s" % filename)
            f.close()
        except IOError:
            self.cons.write("Error writing to file %s" % filename)
        except pickle.PickleError:
            self.cons.write("Error pickling when saving to file %s" % filename)
            
    def load_game(self, filename):
        raise NotImplementedError("Loading games no longer works.")
        if not filename.endswith('.OAD'): 
            filename += '.OAD'
        try:
            f = open(filename, 'r+b')
        except FileNotFoundError:
            self.cons.write("Error, couldn't find file named %s" % filename)
            return
        try:
            backup_ID_dict = Thing.ID_dict.copy()
            Thing.ID_dict.clear()  # unpickling will re-create Thing.ID_dict
            backup_heartbeat_users = self.heartbeat_users.copy()
            self.heartbeat_users.clear()
            saved = pickle.load(f)
            new_ID_dict, newgame = saved
        except pickle.PickleError:
            self.cons.write("Encountered error while loading from file %s, game not loaded." % filename)
            Thing.ID_dict = backup_ID_dict
            self.heartbeat_users = backup_heartbeat_users
            f.close()
            return
        del backup_ID_dict
        # TODO: move below code for deleting player to Player.__del__()
        # Unlink player object from room, contents:
        if self.user.location.extract(self.user):
            dbg.debug("Error deleting player from room during load_game()")
        for o in self.user.contents: 
            if self.user.extract(o):
                dbg.debug("Error deleting contents of player (%s) during load_game()" % o)
        self.cons.user = None
        
        self.user, self.heartbeat_users = newgame.user, newgame.heartbeat_users
        self.user.cons = self.cons  # custom pickling code for Player doesn't save console
        self.cons.user = self.user  # update backref from cons

        for o in Thing.ID_dict: 
            Thing.ID_dict[o]._restore_objs_from_IDs()            

        self.cons.change_players = True

        self.cons.write("Restored game state from file %s" % filename)
    
        f.close()
    
    def save_player(self, filename, player):
        # Uniquify the ID string of every object carried by the player
        tag = '-saveplayer'+str(random.randint(100000,999999))
        l = [player] 
        for obj in l:
            # change object ID and corresponding entry in ID_dict
            del Thing.ID_dict[obj.id]
            obj.id = obj.id + tag  
            obj._add_ID(obj.id)
            # recursively add associated objects
            if obj.contents != None:
                l += obj.contents
            if hasattr(obj, 'default_weapon'):
                l += [obj.default_weapon]
            if hasattr(obj, 'default_armor'):
                l += [obj.default_armor]

        if not filename.endswith('.OADplayer'): 
            filename += '.OADplayer'
        try:
            f = open(filename, 'w')
            # XXX double-check: is this really necessary? 
            backup_ID_dict = Thing.ID_dict.copy()
            Thing.ID_dict.clear()
            # change location & contents etc from obj reference to ID:
            for obj in l:
                obj._change_objs_to_IDs()
            saveables = [x.get_saveable() for x in l]
            f.write(json.dumps(saveables, sort_keys=True, indent=4))
            Thing.ID_dict = backup_ID_dict
            player.cons.write("Saved player data to file %s" % filename)
            f.close()
        except IOError:
            player.cons.write("Error writing to file %s" % filename)
        # restore location & contents etc to obj references:
        for obj in l:
            obj._restore_objs_from_IDs()
        # restore original IDs by removing tag
        for obj in l:
            del Thing.ID_dict[obj.id]  # get rid of uniquified entry in ID_dict
            (head, sep, tail) = obj.id.partition(tag)
            obj.id = head  
            obj._add_ID(obj.id)  # re-create original entry in ID_dict
        

    def load_player(self, filename, cons, oldplayer=None):
        """Load a single player and his/her inventory from a saved file.

        Objects in the player's inventory (and their contents, recursively) 
        are treated as new objects, and will often be duplicates of
        existing objects already in the game. Thus after unpickling each 
        object we need to add it to Thing.ID_dict with a new and unique ID.""" 


        if not filename.endswith('.OADplayer'): 
            filename += '.OADplayer'
        try:
            f = open(filename, 'r')
        except FileNotFoundError:
            cons.write("Error, couldn't find file named %s" % filename)
            raise gametools.PlayerLoadError
        try:
            # l is the list of objects (player + recursive inventory). Note that 
            # the loading code calls init() which creates new entries in ID_dict for objects in l,
            # using the uniquified IDs - guaranteed to succeed without further changing ID
            saveables = json.loads(f.read())
            f.close()
            l = []
            for x in saveables:
                obj = gametools.clone(x['path'])
                obj.update_obj(x)
                l.append(obj)
        except EOFError:
            cons.write("The file you are trying to load appears to be corrupt.")
            raise gametools.PlayerLoadError
        newplayer = l[0]  # first object saved is the player

        if oldplayer:
            # TODO: move below code for deleting player to Player.__del__()
            # Unlink player object from room; delete player along with recursive inventory
            eraselist = [oldplayer]
            for o in eraselist:
                if o.contents:
                    eraselist += o.contents
                if o.location.extract(o):
                    dbg.debug("Error deleting player or inventory during load_game(): object %s contained in %s " % (o, o.location))
                if o in self.heartbeat_users:
                    self.deregister_heartbeat(o)
                del Thing.ID_dict[o.id]
                # o.__del__()  # XXX probably doesn't truly delete the object; needs more research
            cons.user = None
        
        newplayer.cons = cons  # custom saving code for Player doesn't save console
        cons.user = newplayer  # update backref from cons

        cons.change_players = True

        loc_str = newplayer.location
        newplayer.location = gametools.load_room(loc_str) 
        if newplayer.location == None: 
            dbg.debug("Saved location '%s' for player %s no longer exists; using default location" % (loc_str, newplayer), 0)
            cons.write("Somehow you can't quite remember where you were, but you now find yourself back in the Great Hall.")
            newplayer.location = gametools.load_room('domains.school.school.great_hall')

        # Add all of the objects to Thing.ID_dict temporarily
        for o in l:
            Thing.ID_dict[o.id] = o
        
        # Now fix up location & contents[] to list object refs, not ID strings
        for o in l:
            o._restore_objs_from_IDs()
        # Now de-uniquify all IDs, replace object.id and ID_dict{} entry
        for o in l:
            del Thing.ID_dict[o.id]
            (head, sep, tail) = o.id.partition('-saveplayer')
            o.id = o._add_ID(head)  # if object with ID == head exists, will create a new ID

        room = newplayer.location
        room.insert(newplayer)  # insert() does some necessary bookkeeping
        cons.write("Restored game state from file %s" % filename)
        room.report_arrival(newplayer, silent=True)
        room.emit("&nI%s suddenly appears, as if by sorcery!" % newplayer.id, [newplayer])
        return newplayer
    
    def login_player(self, cons):
        """Create a new player object and put it in "login state", which
        doesn't do anything but request the username and password. If the
        username matches a player file, ask for the password, and if they 
        match, load that player. If this is a new username, have them create
        a new password and verify it, then put them in the new character 
        creation room where they will select gender, species, etc. """
        tmp_name = "login_player%d" % random.randint(10000, 99999)
        user = gametools.clone('player', [tmp_name, cons])
        cons.user = user
        cons.write("Please enter your username: ")
        user.login_state = "AWAITING_USERNAME"

    def register_heartbeat(self, obj):
        """Add the specified object (obj) to the heartbeat_users list"""
        if obj not in self.heartbeat_users:
            self.heartbeat_users.append(obj)
        else:
            dbg.debug("object %s is already in the heartbeat_users list!" % obj, 2)
    
    def deregister_heartbeat(self, obj):
        """Remove the specified object (obj) from the heartbeat_users list"""
        if obj in self.heartbeat_users:
            del self.heartbeat_users[self.heartbeat_users.index(obj)]
        else:
            dbg.debug("object %s, not in heartbeat_users, tried to deregister heartbeat!" % obj, 2)

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

    
    def beat(self):
        """Advance time, run scheduled events, and call registered heartbeat functions"""
        self.time += 1
        if self.run_timings:
            self.runtime = time.time() - self.last_seconds
            self.last_seconds = time.time()
            dbg.debug("Last runthrough took %s seconds." % self.runtime, 4)
        dbg.debug("Beat! Time = %s" % self.time, 4)
        
        current_events = self.events.check_for_event(self.time)            
        for event in current_events:
            if (self.handle_exceptions):
                try:
                    event.callback(event.payload)
                except Exception as inst:
                    dbg.debug("An error occured while attepting to complete event (timestamp %s, callback %s, payload %s)! Printing below:" % (event.timestamp, event.callback, event.payload), 0)
                    dbg.debug(traceback.format_exc(), 0)
                    dbg.debug('Error caught!', 0)
            else:
                event.callback(event.payload)

        for h in self.heartbeat_users:
            if (self.handle_exceptions):
                try:
                    h.heartbeat()
                except Exception as inst:
                    dbg.debug("An error occured inside code for %s! Printing below:" % h, 0)
                    dbg.debug(traceback.format_exc(), 0)
                    dbg.debug('Error caught!', 0)
            else:
                h.heartbeat()
        self.runtime = time.time() - self.last_seconds
        self.last_seconds = time.time()

        # schedule the next heartbeat:
        asyncio.get_event_loop().call_later(1,self.beat)

    
    def check_char(self):
        """Checks to see if there is any keyboard input, and if so, directs it to the game console."""
        # check for keyboard entries
        if self.kb.kbhit():
            self.answer_kbd_input()

        asyncio.get_event_loop().call_later(0.1, self.check_char)


    def answer_kbd_input(self):
        """Answer keyboard input pertaining to the game console."""
        key = self.kb.getch()
        if (ord(key) >= 48 and ord(key) <= 57) or (ord(key) >= 97 and ord(key) <= 122) or ord(key) == 32: #lowercase letters, numbers, and spaces
            if not self.current_input_str:
                print(self.current_prompt, end='', flush=True)
            print(key, end='', flush=True)
            self.current_input_str += key
        
        elif ord(key) == 10: # enter
            if not self.current_input_str:
                pass
            else:
                try:
                    self.commands[self.current_input_str.split()[0]](self.current_input_str)
                    self.current_input_str = ''
                    print('\n', end='', flush=True)
                except KeyError:
                    print('\nInvalid command. Please try again.')
                    self.current_input_str = ''
                except Exception:
                    print('\nAn exception occured.')
                    print(traceback.format_exc())
                    self.current_input_str = ''

        elif ord(key) == 127: # backspace
            if not self.current_input_str:
                pass
            else:
                print('\nCharacter deleted\n', end='', flush=True)
                input_lst = [x for x in self.current_input_str]
                self.current_input_str = ''
                input_total_len = len(input_lst)
                for num in range(0, input_total_len):
                    x = input_lst[0]
                    i = input_lst.index(x)
                    length = len(input_lst) - 1
                    if i != length:
                        self.current_input_str += x
                    del input_lst[input_lst.index(x)]
                if self.current_input_str:
                    print(self.current_prompt, self.current_input_str, sep='', end='', flush=True)
        else:
            print('\nPlease use only lowercase letters, numbers, and newlines.')
            if self.current_input_str:
                print(self.current_prompt, self.current_input_str, sep='', end='', flush=True)
        
        if self.kb.kbhit():
            self.answer_kbd_input()

    def quit_game(self, msg):
        """Quits the game. Requires a confirm command from the game console."""
        print('Are you sure you want to quit? The game will not be saved.')
        confirm = input('Click enter to cancel. Any value will confirm:')
        if confirm:
            asyncio.get_event_loop().stop()

    def print_help_msg(self, msg):
        print(self.current_msg, self.commands, sep='\n')

    def set_dbg_verbosity(self, msg):
        print('\n', end='', flush=True)
        words = msg.split()
        try:
            level = int(words[1])
        except IndexError:
            print(self._set_verbosity())
            return
        except ValueError:
            if words[1] == 'filter':
                try:
                    s = words[2:] 
                    dbg.set_filter_str(s)
                    print("Set verbose filter to '%s', debug strings containing '%s' will now be printed." % (s, s))                      
                except IndexError:
                    dbg.set_filter_str('&&&')
                    print("Turned off verbose filter; debug messages will only print if they are below level %d." % dbg.verbosity)
                return
            print("Usage: verbose [level]\n    Toggles debug message verbosity on and off (level 1 or 0), or sets it to the optionally provided <level>")
            return
        except Exception:
            print(traceback.format_exc())
        print(self._set_verbosity(level))


    def start_loop(self, message=None, port=9124):
        print(message if message else "Starting game...")
        asyncio.get_event_loop().run_until_complete(
            websockets.serve(connections_websock.ws_handler, self.ip_address, port))
        print("Listening on port %s..." % port)
        asyncio.get_event_loop().call_later(1,self.beat)
        asyncio.get_event_loop().call_later(1.05,self.check_char)
        asyncio.get_event_loop().run_forever()
        # XXX add callbacks to handle game exit? 
        dbg.debug("Exiting main game loop!")
        dbg.shut_down()

    def begin_analysis_mode(self):
        dbg.verbosity = 4
        self.run_timings = True

        self.start_loop('Starting game in analysis mode...')

    def clear_nulspace(self, x): #XXX temp problem events always returns a payload, often None.
        dbg.debug("Game.clear_nulspace() called! Currently does nothing.")
        '''
        for i in self.nulspace.contents:
            if not hasattr(i, 'cons'): #if it is not player
                i.delete()
        self.events.schedule(self.time+5, self.clear_nulspace)
        '''
