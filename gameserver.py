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
from console import Console
from parse import Parser

class Game():
    """
        The Game class contains a parser, a list of players, a time counter, 
        a list of objects that have a heartbeat (a function that runs 
        periodically), and the IP address of the server. 
    """
    def __init__(self, server=None, mode=False, duration=86400, port=9124):
        Thing.game = self  # only one game instance ever exists, so no danger of overwriting this
        self.log = gametools.get_game_logger("_gameserver")
        self.acl = miracle.Acl()
        self.set_up_groups_and_acl()
        self.server_ip = server  # IP address of server, if specified
        self.is_ssl = ('ssl' in mode) or ('https' in mode)
        self.encryption_setting = not ('nocrypt' in mode or 'no' in mode or 'noencrypt' in mode)
        if connections_websock.encryption_installed:
            connections_websock.encryption_enabled = self.encryption_setting
        self.keep_going = True  # game ends when set to False
        self.start_time = 0
        try:
            self.duration = int(duration)
        except ValueError:
            self.duration = 86400
        except TypeError:
            self.duration = 86400
        try:
            self.port = port
        except ValueError:
            self.port = 9124
        except TypeError:
            self.port = 9124
        
        self.heartbeat_users = []  # objects to call "heartbeat" callback every beat
        self.time = 0  # number of heartbeats since game began
        self.events = asyncio.get_event_loop()

        self.parser = Parser()
        self.users = []

        self.shutdown_console = None

        self.total_times = {}
        self.numrun_times = {}
        self.maximum_times = {}
    
    def get_file_privileges(self, player_name, path, check_type='read'):
        """Return True if the given player belongs to any groups that have 
        the specified permission ('read' or 'edit') on the specified file. 
        Tests the given filename first, then repeatedly tests the containing
        directory up to & including the root ('/') of the game filesystem."""        
        groups = self.wizards[player_name]
        path = gametools.expandGameDir(path, player_name)  # expand ~ aliases
        path = gametools.normGameDir(path)  # collapse redundant /'s and ..'s
        # See whether any of the groups player belongs to has permission.
        # Note acl.check_any() returns False if any parameters don't exist
        if self.acl.check_any(groups, path, check_type):  
            return True
        while path != '/':
            trunc_path = os.path.dirname(path)  # truncate path to containing dir
            if trunc_path == path: 
                break  # no more / to truncate
            path = trunc_path
            if self.acl.check_any(groups, path, check_type):  
                return True
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
    
    def save_player(self, filename, player):
        try:
            player.save_cons_attributes()
        except Exception:
            self.log.error('Error saving console attributes for player %s!' % player)

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
                self.log.error('Error uniquifying the ID of %s. Removing from player inventory.' % obj)
                broken_objs.append(obj)
                
        for obj in broken_objs:
            try:
                obj.destroy()
            except Exception:
                self.log.exception('Error destroying object %s!' % obj)
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
            f.write(json.dumps(saveables, skipkeys=True, sort_keys=True, indent=4))
            Thing.ID_dict = backup_ID_dict
            player.cons.write("Saved player data to file %s" % filename)
            f.close()
        except IOError:
            player.cons.write("Error writing to file %s" % filename)
            Thing.ID_dict = backup_ID_dict # ESSENTIAL THAT WE DO THIS!
        except TypeError:
            player.cons.write("Error writing to file %s" % filename)
            self.log.exception('A TypeError occured while trying to save player %s. Printing below:' % player)
            Thing.ID_dict = backup_ID_dict
        # restore location & contents etc to obj references:
        for obj in l:
            try:
                obj._restore_objs_from_IDs()
            except Exception:
                broken_objs.append(obj)
                self.log.exception('An error occured while loading %s! Printing below:')

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
                    self.log.error("Error deleting player or inventory during load_game(): object %s contained in %s " % (o, o.location))
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
            self.log.warning("Saved location '%s' for player %s no longer exists; using default location" % (loc_str, newplayer))
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
                self.log.exception('An error occured while loading %s! Printing below:')
        # Now de-uniquify all IDs, replace object.id and ID_dict{} entry
        for o in l:
            try:
                del Thing.ID_dict[o.id]
                (head, sep, tail) = o.id.partition('-saveplayer')
                o.id = o._add_ID(head)  # if object with ID == head exists, will create a new ID
            except Exception:
                broken_objs.append(o)
                self.log.exception('An error occured while loading %s! Printing below:')

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
            cons.write("Restored game state from file %s" % filename)
            room.report_arrival(newplayer, silent=True)
            room.emit("&nI%s suddenly appears, as if by sorcery!" % newplayer.id, [newplayer])
        except Exception:
            self.log.error('Error inserting player into location! Moving player back to default start location')
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
    
    def get_profiling_report(self):
        report_str = ''
        all_time_spent = sum([self.total_times[x] for x in self.total_times])
        for i in self.total_times:
            report_str += '\n%s:\n' % i
            report_str += 'Total time running: %s\n' % self.total_times[i]
            if i in self.maximum_times:
                report_str += 'Average time running: %s\n' % ((self.total_times[i])/(self.numrun_times[i]))
                report_str += 'Maximum time running: %s\n' % self.maximum_times[i]
            report_str += 'Percentage of total time: %s\n' % ((self.total_times[i]/all_time_spent)*100)
        return report_str

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
        profile_st = time.time()
        try:
            func(*params)
        except:
            self.log.exception("An error occured while attepting to complete event (timestamp %s, callback %s, payload %s)! Printing below:" % (self.time, func, [*params]))
        profile_et = time.time()
        profile_t = profile_et - profile_st
        funcname = str(func).replace('<','[').replace('>',']')
        if funcname in self.total_times:
            self.total_times[funcname] += profile_t
            self.numrun_times[funcname] += 1
            if profile_t > self.maximum_times[funcname]:
                self.maximum_times[funcname] = profile_t
        else:
            self.total_times[funcname] = profile_t
            self.numrun_times[funcname] = 1
            self.maximum_times[funcname] = profile_t
        self.log.debug("Function %s took %s seconds" % (funcname, profile_t))
        
    
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
        if self.is_ssl:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ssl_context.load_default_certs()
            ssl_context.load_cert_chain("certificate.pem", "private_key.pem")
            ssl_context.set_ciphers("ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305-SHA256:ECDHE-RSA-CHACHA20-POLY1305-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-RSA-AES256-SHA:RSA-AES128-GCM-SHA256:RSA-AES256-GCM-SHA384:RSA-AES128-SHA:RSA-AES256-SHA:RSA-3DES-EDE-SHA")
            self.events.run_until_complete(
                websockets.serve(connections_websock.ws_handler, self.server_ip, 9124, ssl=ssl_context))
        else:
            self.events.run_until_complete(websockets.serve(connections_websock.ws_handler, self.server_ip, 9124))


    def start_loop(self):
        # Keep track of game start time to support periodic reboots 
        # and to serve as a random seed for various things
        self.start_time = time.time()
        print("Starting game...")

        while not self.server_ip:
            input_ip = input('IP Address: ')
            try:  # validate the ip address passed as an argument, if any
                ipaddress.ip_address(input_ip)
                self.server_ip = input_ip
            except ValueError:
                print("Error: %s is not a valid IP address! Please try again." % input_ip)
        
        socket_sucessfully_opened = False
        while not socket_sucessfully_opened:
            try:
                self.open_socket()
                socket_sucessfully_opened = True
            except OSError:
                traceback.print_exc()
                time.sleep(4*60)

        print("Listening on %s port 9124..." % self.server_ip)
        self.events.call_later(1,self.beat)
        self.events.run_forever()

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
                self.save_player(gametools.realDir(gametools.PLAYER_DIR, i.names[0]), i)
                i.cons.write('--#quit')
        
        for j in consoles:
            if j and j.user: # Make sure to send all messages from consoles before fully quitting game
                self.events.run_until_complete(connections_websock.ws_send(j))                

        self.log.critical("Exiting main game loop!")
        sys.exit(restart_code)
