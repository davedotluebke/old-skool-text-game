import io
import os
import sys
import traceback
import random
import time
import asyncio
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

class Game():
    """
        The Game class contains a parser, a list of players, a time counter, 
        a list of objects that have a heartbeat (a function that runs 
        periodically). It should also probably house the Twisted event loop 
        and associated factory for creating protocols (connections to clients)
    """
    def __init__(self):
        Thing.game = self  # only one game instance ever exists, so no danger of overwriting this
        self.keep_going = True  # game ends when set to False
        self.handle_exceptions = True # game will catch all exceptions rather than let debugger handle them
        self.start_time = 0
        
        self.heartbeat_users = []  # objects to call "heartbeat" callback every beat
        self.time = 0  # number of heartbeats since game began
        self.events = EventQueue()  # events to occur in future 

        self.parser = Parser()
        self.dbg = dbg
        self.users = []

        self.shutdown_console = None
        self.player_read_privilages = {'scott':['.*']}     # Note: administrators are responsible for making sure that 
        self.player_edit_privilages = {'scott':['domains.*','home/scott.*']} # wizards can view and edit their own files

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
    
    def create_backups(self, filename, player, other_filename):        
        if not other_filename.endswith('.OADplayer'):
            other_filename += '.OADplayer'
        
        former_files = []
        try:
            f = open(other_filename, 'r')
            former_files.append(f.read())
            f.close()
        except FileNotFoundError:
            return
        
        for i in range(0, 20):
            try:
                f = open(filename+str(i)+'.OADplayer', 'r')
                former_files.append(f.read())
                f.close()
            except FileNotFoundError:
                pass
        
        for j in range(0, len(former_files)):
            try:
                f = open(filename+str(j)+'.OADplayer', 'w')
                f.write(former_files[j])
                f.close()
            except FileNotFoundError:
                pass
    
    def save_player(self, filename, player):
        try:
            player.save_cons_attributes()
        except Exception:
            dbg.debug('Error saving console attributes for player %s!' % player, 0)

        # Keep a list of "broken objects" to destroy
        broken_objs = []
        # Uniquify the ID string of every object carried by the player
        tag = '-saveplayer'+str(random.randint(100000,999999))
        l = [player] 
        for obj in l:
            # change object ID and corresponding entry in ID_dict
            try:
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
            except Exception:
                dbg.debug('Error uniquifying the ID of %s. Removing from player inventory.' % obj)
                broken_objs.append(obj)
                
        for obj in broken_objs:
            try:
                obj.destroy()
            except Exception:
                dbg.debug('Error destroying object %s!' % obj, 0)
                # TODO: figure out what to do here

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
            try:
                obj._restore_objs_from_IDs()
            except Exception:
                broken_objs.append(obj)
                dbg.debug('An error occured while loading %s! Printing below:', 0)
                dbg.debug(traceback.format_exc(), 0)
                dbg.debug('Error caught!', 0)

        # restore original IDs by removing tag
        for obj in l:
            del Thing.ID_dict[obj.id]  # get rid of uniquified entry in ID_dict
            (head, sep, tail) = obj.id.partition(tag)
            obj.id = head  
            obj._add_ID(obj.id)  # re-create original entry in ID_dict
        

    def load_player(self, filename, cons, oldplayer=None, password=None):
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
                if not obj:
                    continue
                del Thing.ID_dict[obj.id] # Delete the temporary ID created by the `clone` function
                obj.update_obj(x)
                l.append(obj)
        except EOFError:
            cons.write("The file you are trying to load appears to be corrupt.")
            raise gametools.PlayerLoadError
        newplayer = l[0]  # first object saved is the player
        if password:
            if password != newplayer.password:
                raise gametools.IncorrectPasswordError
        
        broken_objs = [] # Make sure to remove all of the broken objects from the player's inventory

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
        newplayer.update_cons_attributes()

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
            try:
                o._restore_objs_from_IDs()
            except Exception:
                broken_objs.append(o)
                dbg.debug('An error occured while loading %s! Printing below:', 0)
                dbg.debug(traceback.format_exc(), 0)
                dbg.debug('Error caught!', 0)
        # Now de-uniquify all IDs, replace object.id and ID_dict{} entry
        for o in l:
            try:
                del Thing.ID_dict[o.id]
                (head, sep, tail) = o.id.partition('-saveplayer')
                o.id = o._add_ID(head)  # if object with ID == head exists, will create a new ID
            except Exception:
                broken_objs.append(o)
                dbg.debug('An error occured while loading %s! Printing below:', 0)
                dbg.debug(traceback.format_exc(), 0)
                dbg.debug('Error caught!', 0)

        # Make sure that broken objects are removed from their container's contents list
        reference_check = [newplayer]
        for obj in reference_check:
            if obj.contents and isinstance(obj.contents, list):
                for o in obj.contents:
                    if o in broken_objs:
                        del obj.contents[obj.contents.index(o)]
                    # Catch a few specific errors
                    if o.location != obj:
                        broken_objs.append(o)
                        del obj.contents[obj.contents.index(o)]
        
        for o in broken_objs:
            try:
                o.destroy()
            except Exception:
                dbg.debug('Error destroying object %s!' % o, 0)
                #TODO: Figure out what to do here

        room = newplayer.location
        try:
            room.insert(newplayer)  # insert() does some necessary bookkeeping
            cons.write("Restored game state from file %s" % filename)
            room.report_arrival(newplayer, silent=True)
            room.emit("&nI%s suddenly appears, as if by sorcery!" % newplayer.id, [newplayer])
        except Exception:
            dbg.debug('Error inserting player into location! Moving player back to default start location', 0)
            room = gametools.load_room(newplayer.start_loc_id)
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
    
    def beat(self):
        """Advance time, run scheduled events, and call registered heartbeat functions"""
        self.time += 1
        dbg.debug("Beat! game.time = %s" % self.time, 4)
        dbg.debug("Time since game began (in seconds): %s" % (time.time() - self.start_time), 4)
        
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
        
        if time.time() > (self.start_time + 86400):
            self.keep_going == False
        
        if self.keep_going:
            # schedule the next heartbeat
            asyncio.get_event_loop().call_later(1,self.beat)
        else:
            # quit the game
            asyncio.get_event_loop().stop()

    def start_loop(self):
        # To have a consistant 24 hour shutdown time
        # The start time is always the last midnight the occured.
        self.start_time = (time.time() // 86400)*86400
        print("Starting game...")
        ip_address = input('IP Address: ')
        asyncio.get_event_loop().run_until_complete(
            websockets.serve(connections_websock.ws_handler, ip_address, 9124))
        print("Listening on port 9124...")
        asyncio.get_event_loop().call_later(1,self.beat)
        asyncio.get_event_loop().run_forever()
        # XXX add callbacks to handle game exit?
        # Go through and save every player
        players = [Thing.ID_dict[x] for x in Thing.ID_dict if isinstance(Thing.ID_dict[x], Player)]
        consoles = [x.cons for x in players]
        restart_code = 0
        if self.shutdown_console:
            consoles.append(self.shutdown_console)
            restart_code = 1
        for i in players:
            if i.cons:
                i.cons.write('The game is now shutting down.')
                self.save_player(os.path.join(gametools.PLAYER_DIR, i.names[0]), i)
                i.cons.write('#quit')
        
        for j in consoles:
            if j: # Make sure to send all messages from consoles before fully quitting game
                asyncio.get_event_loop().run_until_complete(connections_websock.ws_send(j))                

        dbg.debug("Exiting main game loop!")
        dbg.shut_down()
        sys.exit(restart_code)

    def clear_nulspace(self, x): #XXX temp problem events always returns a payload, often None.
        dbg.debug("Game.clear_nulspace() called! Currently does nothing.")
        '''
        for i in self.nulspace.contents:
            if not hasattr(i, 'cons'): #if it is not player
                i.delete()
        self.events.schedule(self.time+5, self.clear_nulspace)
        '''
