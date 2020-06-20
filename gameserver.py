import io
import os
import sys
import ipaddress
import random
import re
import time
import asyncio
import pathlib
import ssl
import functools
import json
import pprint

import websockets
import connections_websock
import miracle

import gametools

from thing import Thing
from player import Player
from parse import Parser
from parse import Parser

class Game():
    """
        The Game class contains a parser, a list of players, a time counter, 
        a list of objects that have a heartbeat (a function that runs 
        periodically), and the IP address of the server. 
    """
    def __init__(self, server=None, duration=86400, port=9124, retry=5, silent=False):
        Thing.game = self  # only one game instance ever exists, so no danger of overwriting this
        self.server_ip = server  # IP address of server, if specified
        # print gameserver log messages to stderr only on localhost
        self.log = gametools.get_game_logger("_gameserver", printing=(self.server_ip == '127.0.0.1'))
        self.acl = miracle.Acl()
        self.set_up_groups_and_acl()
        self.keep_going = True  # game ends when set to False
        self.start_time = 0
        try:
            self.duration = int(duration)
        except:
            self.log.exception("Error setting game.duration; defaulting to 86400 seconds")
            self.duration = 86400
        try:
            self.port = port
        except:
            self.log.exception("Error setting game.port; defaulting to 9124")
            self.port = 9124
        try: 
            self.retry = int(retry)
        except:
            self.log.exception("Error setting game.retry; defaulting to 5")
            self.retry = 5
        
        self.heartbeat_users = []  # objects to call "heartbeat" callback every beat
        self.time = 0  # number of heartbeats since game began
        self.events = asyncio.get_event_loop()

        self.parser = Parser()

        self.total_times = {}
        self.numrun_times = {}
        self.maximum_times = {}
    
    #
    # Permissions and File Manipulation section
    #
    
    def get_file_privileges(self, player_name, path, check_type='read'):
        """Return True if the given player belongs to any groups that have 
        the specified permission ('read' or 'write') on the specified file. 
        Tests the given filename first, then repeatedly tests the containing
        directory up to & including the root ('/') of the game filesystem."""        
        groups = self.wizards[player_name]
        path = gametools.expandGameDir(path, player_name)  # expand ~ aliases
        path = gametools.normGameDir(path)  # collapse redundant /'s and ..'s
        # See whether any of the groups player belongs to has permission.
        # Note acl.check_any() returns False if any parameters don't exist
        if self.acl.check_any(groups, path, check_type):  
            return True
        # If there are permissions set on the given file, we don't want to
        # continue checking higher levels. If there are not, we do want this
        if self.acl.get_permissions(path):
            return False
        while path != '/':
            trunc_path = os.path.dirname(path)  # truncate path to containing dir
            if trunc_path == path: 
                break  # no more / to truncate
            path = trunc_path
            if self.acl.check_any(groups, path, check_type):  
                return True
            if self.acl.get_permissions(path):
                return False
        return False

    def get_read_privileges(self, player_name, path):
        return self.get_file_privileges(player_name, path)

    def get_edit_privileges(self, player_name, path):
        return self.get_file_privileges(player_name, path, check_type='write')

    def is_wizard(self, player_name):
        """Return True if the specified player is a wizard."""
        return player_name in self.wizards

    def set_up_groups_and_acl(self):
        # default list of administrators and wizards, will be overwritten if PLAYER_ROLES_FILES exists 
        self.roles = {"admin": ["scott", "cedric"], "wizard": ["scott", "cedric"], "apprentice": [], "scott": ["scott"], "cedric": ["cedric"]}
        self.wizards = {"scott":["scott", "wizard", "admin"], "cedric":["cedric", "wizard", "admin"]}
        try:
            f = open(gametools.realDir(gametools.PLAYER_ROLES_FILE))
            player_roles = json.loads(f.read())
            f.close()
            self.roles = player_roles['roles']
            self.wizards = player_roles['wizards']
        except FileNotFoundError: 
            self.log.error("Couldn't open player_roles file '%s'; using default roles and wizards" % gametools.PLAYER_ROLES_FILE)
        except AttributeError:
            self.log.error("Error reading data from player_roles; attempting to use default roles & wizards")

        self.acl.add_roles(self.roles.keys())
        # create permissions for each wizard's home directory:
        for w in self.wizards.keys():  
            self.acl.add({gametools.HOME_DIR+w: ('read', 'write')})  
            self.acl.grant(w, gametools.HOME_DIR+w, 'read')
            self.acl.grant(w, gametools.HOME_DIR+w, 'write')
            self.acl.grant('admin', gametools.HOME_DIR+w, 'read')
            self.acl.grant('admin', gametools.HOME_DIR+w, 'write')
        # create permissions for each domain:
        for d in [x.name for x in os.scandir(gametools.realDir(gametools.DOMAIN_DIR)) if x.is_dir() and x.name != '__pycache__'] :
            self.acl.add({gametools.DOMAIN_DIR+d: ('read', 'write')})
            self.acl.grant(d, gametools.DOMAIN_DIR+d, 'read')
            self.acl.grant(d, gametools.DOMAIN_DIR+d, 'write')
            self.acl.grant('admin', gametools.DOMAIN_DIR+d, 'read')
            self.acl.grant('admin', gametools.DOMAIN_DIR+d, 'write')
        # everyone can read core game files, but not write
        self.acl.add({'/': ('read', 'write')})
        self.acl.grant('admin', '/', 'read')
        self.acl.grant('admin', '/', 'write')
        self.acl.grant('wizard', '/', 'read')
        self.acl.add({'/saved_players': ('read', 'write')})
        self.acl.grant('admin', '/saved_players', 'read')
        self.acl.grant('admin', '/saved_players', 'write')
        self.acl.add({'/backup_saved_players': ('read', 'write')})
        self.acl.grant('admin', '/backup_saved_players', 'read')
        
        """
        self.acl.add_resource('wiz_commands')       # apparate, reload, emote
        self.acl.add_resource('code_commands')      # clone, fetch
        self.acl.add_resource('execute')            # execute an arbitrary Python command
        self.acl.add_resource('edit_own_files')     # edit files in wizard's home directory
        self.acl.add_resource('edit_domain_files')  # edit files in wizard's domain
        self.acl.add_resource('player_actions')     # reset password & domain; edit player save files
        """
    
    def add_wizard_role(self, wizard, role):
        """Associate a player with a given role (e.g. the "admins" role or "wizards" role)"""
        self.wizards.setdefault(wizard, []).append(role)
        self.roles.setdefault(role, []).append(wizard)
        self.log.info("Added player %s to role %s" % (wizard, role))

    def remove_wizard_role(self, wizard, role):
        """Disassociate a player from a given role"""
        try: 
            self.wizards[wizard].remove(role)
            self.roles[role].remove(wizard)
        except KeyError:
            self.log.error("Couldn't disassociate wizard %s from role %s" % (wizard, role))

    def list_wizard_roles(self, wiz=None, role=None):
        """Return a human-readable string listing:
        - the roles for the specified wizard, if any, and
        - the wizards in the specified role, if any; 
        If neither wizard or role is specified, list all wizards and all roles.\n"""
        msg = ""
        if wiz:
            try:
                msg += "```game.wizards[%s] = %s```\n" % (wiz, pprint.pformat(self.wizards[wiz], width=40, indent=4))
            except: 
                msg += "No wizard '%s' in `game.wizards[]`\n" % wiz
        if role: 
            try:
                msg += "```game.roles[%s] = %s```\n" % (role, pprint.pformat(self.roles[role], width=40, indent=4))
            except: 
                msg += "No role '%s' in `game.roles[]`\n" % role
        if not wiz and not role:
            msg += "```game.wizards[] = %s```\n" % pprint.pformat(self.wizards, width=40, indent=4)
            msg += "```game.roles[] = %s```\n" % pprint.pformat(self.roles, width=40, indent=4)
        return msg
    
    #
    # Saving and loading section
    #

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
            self.log.error("Error deleting player from room during load_game()")
        for o in self.user.contents: 
            if self.user.extract(o):
                self.log.error("Error deleting contents of player (%s) during load_game()" % o)
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
        """Makes up to 20 backups of <filename>. 
        NOTE: filenames are real filesystem paths, not game filesystem."""
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
    
    def is_jsonable(self, x):
        """Test to see if an item is json-serialisable. Used as a last resort to prevent players from not saving."""
        try:
            json.dumps(x)
            return True
        except (TypeError, OverflowError):
            return False
    
    def save_player(self, player, access_point):
        """Create a saveable dictionary representing the player object and everything they are carrying. 
        This will be sent to the console for saving. NOTE: This code has several critical sections, and 
        must be run synchronously."""
        # Keep a list of "broken objects" to destroy
        broken_objs = []
        # Uniquify the ID string of every object carried by the player
        tag = '-saveplayer'+str(random.randint(100000,999999))
        l = [player] 
        for obj in l:
            # change object ID and corresponding entry in ID_dict
            try:
                obj.id = obj.id + tag  
                obj._add_ID(obj.id, remove_existing=True)
                # recursively add associated objects
                if obj.contents != None:
                    l += obj.contents
                if hasattr(obj, 'default_weapon'):
                    l += [obj.default_weapon]
                if hasattr(obj, 'default_armor'):
                    l += [obj.default_armor]
            except Exception:
                self.log.error('Error uniquifying the ID of %s. Removing from player inventory.' % obj)
                broken_objs.append(obj)
                
        for obj in broken_objs:
            try:
                obj.destroy()
            except Exception as e:
                self.log.exception('Error destroying object %s!' % obj)
                # TODO: figure out what to do here

        for obj in l:
            obj._change_objs_to_IDs()
        saveables = [x.get_saveable() for x in l]
        for i in saveables:
            sub_amt = 0
            for sidx in range(0, len(i)):
                j = list(i.keys())[sidx - sub_amt]
                if not self.is_jsonable(i[j]):
                    del i[j]
                    sub_amt += 1
        player_json = json.dumps(saveables, skipkeys=True, sort_keys=True, indent=4)
        access_point.send_message("Saved player data!")
        player.log.info("Returning player data to access point")
        # restore location & contents etc to obj references:
        for obj in l:
            try:
                obj._restore_objs_from_IDs()
            except Exception:
                broken_objs.append(obj)
                self.log.exception('An error occurred while loading %s! Printing below:')

        # restore original IDs by removing tag
        for obj in l:
            del Thing.ID_dict[obj.id]  # get rid of uniquified entry in ID_dict
            (head, sep, tail) = obj.id.partition(tag)
            obj.id = head  
            obj._add_ID(obj.id)  # re-create original entry in ID_dict
        
        return player_json # this will be sent by calling function
        

    def load_player(self, player_json, access_point):
        """Load a player from the player_json string and add them to the game. 
        In addition to loading, this function will return the player. 
        NOTE: This code contains several critical sections and must be run synchronously."""

        # l is the list of objects (player + recursive inventory). Note that 
        # the loading code calls init() which creates new entries in ID_dict for objects in l,
        # using the uniquified IDs - guaranteed to succeed without further changing ID
        saveables = json.loads(player_json)
        l = []
        for x in saveables:
            obj = gametools.clone(x['path'])
            if not obj:
                continue
            del Thing.ID_dict[obj.id] # Delete the temporary ID created by the `clone` function
            obj.update_obj(x)
            l.append(obj)
        newplayer = l[0]  # first object saved is the player
        
        broken_objs = [] # Make sure to remove all of the broken objects from the player's inventory

        loc_str = newplayer.location
        newplayer.location = gametools.load_room(loc_str) 
        if newplayer.location == None: 
            self.log.warning("Saved location '%s' for player %s no longer exists; using default location" % (loc_str, newplayer))
            access_point.send_message("Somehow you can't quite remember where you were, but you now find yourself somewhere else.")
            newplayer.location = gametools.load_room(gametools.DEFAULT_START_LOC)

        # Add all of the objects to Thing.ID_dict temporarily
        for o in l:
            Thing.ID_dict[o.id] = o
        
        # Now fix up location & contents[] to list object refs, not ID strings
        for o in l:
            try:
                o._restore_objs_from_IDs()
            except Exception:
                broken_objs.append(o)
                self.log.exception('An error occurred while loading %s! Printing below:')
        # Now de-uniquify all IDs, replace object.id and ID_dict{} entry
        for o in l:
            try:
                del Thing.ID_dict[o.id]
                (head, sep, tail) = o.id.partition('-saveplayer')
                o.id = o._add_ID(head)  # if object with ID == head exists, will create a new ID
            except Exception:
                broken_objs.append(o)
                self.log.exception('An error occurred while loading %s! Printing below:')

        # Make sure that broken objects are removed from their container's contents list
        reference_check = [newplayer]
        for obj in reference_check:
            if obj.contents and isinstance(obj.contents, list):
                for o in obj.contents:
                    if o in broken_objs:
                        del obj.contents[obj.contents.index(o)]
                    # Catch a few specific errors
                    try:
                        if o.location != obj:
                            broken_objs.append(o)
                            del obj.contents[obj.contents.index(o)]
                    except ValueError:
                        broken_objs.append(o)
        
        for o in broken_objs:
            try:
                o.destroy()
            except Exception:
                self.log.error('Error destroying object %s!' % o)
                #TODO: Figure out what to do here

        room = newplayer.location
        try:
            room.insert(newplayer)  # insert() does some necessary bookkeeping
            access_point.send_message("Restored player state.")
            room.report_arrival(newplayer, silent=True)
            room.emit("&nI%s suddenly appears, as if by sorcery!" % newplayer.id, [newplayer])
        except Exception:
            self.log.error('Error inserting player into location! Moving player back to default start location')
            room = gametools.load_room(newplayer.start_loc_id)
            access_point.send_message("Restored player state")
            room.report_arrival(newplayer, silent=True)
            room.emit("&nI%s suddenly appears, as if by sorcery!" % newplayer.id, [newplayer])
        return newplayer
    
    #
    # Event Management Functions
    #
    
    def register_heartbeat(self, obj):
        """Add the specified object (obj) to the heartbeat_users list"""
        if obj not in self.heartbeat_users:
            self.heartbeat_users.append(obj)
        else:
            self.log.warning("object %s is already in the heartbeat_users list!" % obj)
    
    def deregister_heartbeat(self, obj):
        """Remove the specified object (obj) from the heartbeat_users list"""
        if obj in self.heartbeat_users:
            del self.heartbeat_users[self.heartbeat_users.index(obj)]
        else:
            self.log.warning("object %s, not in heartbeat_users, tried to deregister heartbeat!" % obj)
    
    def schedule_event(self, delay, func, *params):
        """Helper function to guarentee that all asyncio event calls are in a try/except statement."""
        self.events.call_later(delay, functools.partial(self.catch_func_errs, func, *params))
    
    def catch_func_errs(self, func, *params):
        """Helper function to catch all errors in asyncio events and collect profiling information."""
        profile_st = time.time()
        try:
            func(*params)
        except:
            self.log.exception("An error occurred while attepting to complete event (timestamp %s, callback %s, payload %s)! Printing below:" % (self.time, func, [*params]))
        profile_et = time.time()
        profile_t = profile_et - profile_st
        funcname = ":".join((func.__module__, func.__name__))
        if funcname in self.total_times:
            self.total_times[funcname] += profile_t
            self.numrun_times[funcname] += 1
            if profile_t > self.maximum_times[funcname]:
                self.maximum_times[funcname] = profile_t
        else:
            self.total_times[funcname] = profile_t
            self.numrun_times[funcname] = 1
            self.maximum_times[funcname] = profile_t
        # self.log.debug("Function %s took %s seconds" % (funcname, profile_t))
        
    def log_func_profile(self):
        msg = "Function profiling report\n"
        msg+= "\tFunction name: # of invocations, average time, max time\n"
        for f in self.total_times:
            msg += "%s: %4.2d    %4.2e    %4.2e\n" % (f.rjust(50), self.numrun_times[f], self.total_times[f] / self.numrun_times[f], self.maximum_times[f])
        self.log.info(msg)

    def beat(self):
        """Advance time, run scheduled events, and call registered heartbeat functions"""
        self.time += 1

        for h in self.heartbeat_users:
            self.schedule_event(0, h.heartbeat)

        if time.time() > (self.start_time + self.duration):
            self.keep_going = False
        
        if self.keep_going:
            # schedule the next heartbeat
            self.events.call_later(1,self.beat)
        else:
            # quit the game
            self.events.stop()
    
    def open_socket(self):
        return self.events.run_until_complete(asyncio.create_server(AccessPoint, self.server_ip, self.port))

    def start_loop(self):
        # Keep track of game start time to support periodic reboots 
        # and to serve as a random seed for various things
        self.start_time = time.time()
        self.log.info("Starting game...")

        while not self.server_ip:
            input_ip = input('IP Address: ')
            try:  # validate the ip address passed as an argument, if any
                ipaddress.ip_address(input_ip)
                self.server_ip = input_ip
            except ValueError:
                print("Error: %s is not a valid IP address! Please try again." % input_ip)
        
        for i in range(0, self.retry):
            try:
                server = self.open_socket()
                break
            except:
                self.log.exception(f"Failed to open socket at {self.server_ip}:{self.port}; retrying in 30 seconds")
                time.sleep(30)

        self.log.info("Listening on %s port %d..." % (self.server_ip, int(self.port)))
        self.events.call_later(1,self.beat)
        self.events.run_forever()

        # The following occurs after game exit
        server.close() # XXX all players should be saved and logged out before this
        self.events.run_until_complete(server.wait_closed())
        self.events.close()

        """# Go through and save every player
        players = [Thing.ID_dict[x] for x in Thing.ID_dict if isinstance(Thing.ID_dict[x], Player)]
        consoles = [x.cons for x in players]
        restart_code = 0
        if self.shutdown_console:
            consoles.append(self.shutdown_console)
            restart_code = 1
        for i in players:
            if i.cons:
                i.cons.write('The game is now shutting down.')
                self.save_player(gametools.realDir(gametools.PLAYER_DIR, i.names[0]), i)
                i.cons.write('--#quit')
        
        for j in consoles:
            if j and j.user: # Make sure to send all messages from consoles before fully quitting game
                self.events.run_until_complete(connections_websock.ws_send(j))"""

        self.log.critical("Exiting main game loop!")
        self.log_func_profile()
