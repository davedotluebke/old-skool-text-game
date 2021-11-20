import asyncio
import subprocess
import connections_websock
import secrets
import requests
import os
import re
import platform
import traceback
import shlex

from parse import Parser
from player import Player
import gametools

class Console:
    autosave_interval = 60
    measurement_systems = ['IMP', 'SI']
    default_measurement_system = 'IMP'
    prompt = "--> "
    welcome_message = "Please enter your username: "
    help_msg = """Your goal is to explore the world around you, solve puzzles,
               fight monsters, complete quests, and eventually become a
               Sorcerer capable of changing and adding to the very fabric 
               of the world itself.\n\n
               Useful commands include 'look' to examine your surroundings 
               or an object, 'take' to pick something up, 'inventory' to see 
               what you are carrying, 'go' to move a particular direction. 
               You can use prepositions to create more complex commands and
               adjectives to specify particular objects; articles are 
               optional. Here are some examples of valid commands:\n\n
               \t'look'\n
               \t'go north'\n
               \t'take sword'\n
               \t'take the rusty sword'\n
               \t'drink potion from tall flask'\n
               \t'put the gold coin in the leather bag'\n
               \t'move vines'\n\n
               You can create shortcuts to reduce typing; type 'alias' for 
               more details. Type 'width' to change the console's text width. 
               Type 'quit' to save your progress and leave the game."""

    def __init__(self, net_conn, game = None, encode_str='88838_defaultencodestr_9yq9h'):
        self.game = game
        self.user = None
        self.username = None
        self.login_state = "AWAITING_USERNAME"
        self.raw_input = ''
        self.raw_output = ''
        self.file_input = bytes()
        self.filename_input = ''
        self.file_output = bytes()
        self.filename_output = ''
        self.uploading_filename = ''
        self.current_directory = '/domains'  # always in 'game directory space'
        self.change_players = False
        self.player_commands = []
        self.try_all_console_commands = False
        self.connection = net_conn
        self.input_redirect = None
        self.upload_confirm = True
        self.measurement_system = Console.default_measurement_system
        self.encode_str = str(encode_str)
        self.changing_passwords = False
        self.confirming_replace = False
        self.game.schedule_event(self.autosave_interval, self.save_and_backup)
        self.alias_map = {
            'n':       'go north',
            's':       'go south',
            'e':       'go east', 
            'w':       'go west', 
            'nw':      'go northwest',
            'sw':      'go southwest',
            'ne':      'go northeast',
            'se':      'go southeast',
            'u':       'go up',
            'd':       'go down',
            'i':       'inventory',
            'l':       'look',
            'x':       'execute'
        }

    def detach(self, user):
        if self.user == user:
            self.user = None
        self.login_state = "EXIT"
    
    def _add_alias(self, cmd):
        instructions = 'To create a new alias, type:\n    alias [a] [text]\n' \
                        'where [a] is the new alias and [text] is what will replace the alias.'
         
        if len(self.words) == 1:
            # print a list of current aliases & instructions for adding
            self.write('Current aliases:')
            for a in sorted(self.alias_map, key=self.alias_map.get):
                self.write('%s = %s' % (a.rjust(12), self.alias_map[a]))
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
        expansion = cmd.split(maxsplit=2)[2]    # split off first two words and keep the rest
        self.alias_map[alias] = expansion
        self.write("'%s' is now an alias for '%s'" % (alias, expansion))
        return
    
    def _change_units(self, cmd):
        cmd = cmd.split(' ')
        if len(cmd) == 2:
            if cmd[1].upper() in Console.measurement_systems:
                self.measurement_system = cmd[1].upper()
                self.write('Changed units to %s.' % self.measurement_system)
            else:
                self.write('Not an accepted measurement system. Accepted ones are:\n' + [x for x in Console.measurement_systems])
        else:
            self.write('Current units are: %s\nType units [system] to change them.' % self.measurement_system)

    def _replace_aliases(self):
        if not self.words:  # Return if there are no words to replace with aliases
            return
        replace_words = self.words 
        if replace_words[0] in self.alias_map:
            replace_words[0] = self.alias_map[replace_words[0]]
        return " ".join(replace_words)
    
    def save_and_backup(self, quit_behavior=False):
        """Save the console's player and create backups of previous versions in case the save fails at a later time. Will create an event to call this function again unless
        quit_behavior flag is set to True."""
        self.game.save_player(gametools.realDir(gametools.PLAYER_DIR, self.user.names[0]), self.user)
        self.game.create_backups(gametools.realDir(gametools.PLAYER_BACKUP_DIR, self.user.names[0]), self.user, gametools.realDir(gametools.PLAYER_DIR, self.user.names[0]))
        if not quit_behavior:
            self.game.schedule_event(self.autosave_interval, self.save_and_backup)

    def _handle_login(self, cmd):
        """Handle input for logging in the console."""
        state = self.login_state
        if state == 'AWAITING_USERNAME':
            if  len(cmd.split()) != 1:
                self.write("Usernames must be a single lowercase word with no spaces.\n"
                                "Please enter your username:")
                return
            self.username = cmd.split()[0].lower()  # strips any trailing whitespace
            filename = gametools.realDir(gametools.PLAYER_DIR, self.username) + '.OADplayer'
            try:
                f = open(filename, 'r+b')
                f.close()  # success, player exists, so close file for now & check password
                self.write("Welcome back, %s!\nPlease enter your --#password: " % self.username)
                self.login_state = 'AWAITING_PASSWORD'
            except FileNotFoundError:
                self.write("No player named "+self.username+" found. "
                            "Would you like to create a new player? (yes/no)\n")
                self.login_state = 'AWAITING_CREATE_CONFIRM'
            return
        elif state == 'AWAITING_CREATE_CONFIRM':
            if cmd == "yes": 
                self.write("Welcome, %s!\nPlease create a --#password:" % self.username)
                self.login_state = 'AWAITING_NEW_PASSWORD'
                return
            elif cmd == "no":
                self.write("Okay, please enter your username: ")
                self.login_state = 'AWAITING_USERNAME'
                return
            else:
                self.write("Please answer yes or no: ")
                return
        elif state == 'AWAITING_NEW_PASSWORD':
            passwd = cmd
            # TODO secure password authentication goes here
            self.user = self.game.create_new_player(self, self.username, passwd)
            self.user.log.info("Creating player id %s with default name %s" % (self.user.id, self.user.name()))
            start_room = gametools.load_room(gametools.NEW_PLAYER_START_LOC)
            start_room.insert(self.user, force=True)
            self.user.perceive("\nWelcome to Firefile Sorcery School!\n\n"
            "Type 'look' to examine your surroundings or an object, "
            "'inventory' to see what you are carrying, " 
            "'quit' to end the game, and 'help' for more information.")
            self.login_state = None
            return
        elif state == 'AWAITING_PASSWORD':
            passwd = cmd
            # XXX temporary fix, need more security
            # TODO more secure password authentication goes here
            if self.game.get_existing_player(self.username, passwd):
                self.write("A copy of %s is already in the game. Would you like to take over %s? (yes/no)" % (self.username, self.username))
                self.login_state = 'AWAITING_RECONNECT_CONFIRM'
                return
            filename = gametools.realDir(gametools.PLAYER_DIR, self.username) + '.OADplayer'
            try:
                newuser = self.game.load_player(filename, self, password=passwd)
                newuser.log.info("Loaded player id %s with default name %s" % (newuser.id, newuser.names[0]))
                self.login_state = None
            except gametools.IncorrectPasswordError:
                self.write("Your username or password is incorrect. Please try again.")
                self.login_state = "AWAITING_USERNAME"
            except gametools.PlayerLoadError:
                self.write("Error loading data for player %s from file %s. \n"
                                "Please try again.\nPlease enter your username: " % (self.username, filename))
                self.login_state = "AWAITING_USERNAME"
        elif state == 'AWAITING_RECONNECT_CONFIRM':
            if cmd == 'yes':
                user = self.game.get_existing_player(self.username)
                for websocket in connections_websock.conn_to_client:
                    if connections_websock.conn_to_client[websocket] == self:
                        connections_websock.conn_to_client[websocket] = user.cons
                        user.cons.connection = websocket
                        user.cons.write("Reconnected to player %s" % self.username)
                self.detach()
            elif cmd == 'no':
                self.write("Okay, please enter your username: ")
                self.login_state = "AWAITING_USERNAME"
                return
            elif cmd == 'restart':
                self.write("Erasing existing character and restarting from last save. Please enter your --#password again.")
                user = self.game.get_existing_player(self.username)
                user.destroy()
                self.login_state = "AWAITING_PASSWORD"
            else:
                self.write("Please answer yes or no: ")
                return
    
    def print_welcome_message(self):
        """Print the welcome message in the console, when players first connect."""
        self.write(self.welcome_message)
    
    def _handle_console_commands(self):
        """Handle any commands internal to the console, returning True if the command string was handled."""
        if len(self.words) > 0:
            cmd = self.words[0]
            arg = self.command.partition(' ')[2]  # everything after the command
            path = gametools.expandGameDir(arg, player=self.user.name())
            path = os.path.join(self.current_directory, path)
            path = gametools.normGameDir(path)
            if cmd == 'alias':
                self._add_alias(self.command)
                return True
            
            if cmd == 'units':
                self._change_units(self.command)
                return True
            
            if cmd == 'shell':
                self.try_all_console_commands = not self.try_all_console_commands
                self.write(f'Toggled shell mode to {"on" if self.try_all_console_commands else "off"}')
                return True
            
            if cmd == 'help':
                self.write(self.help_msg)
                return True

            if cmd == 'profile':
                # check wizard privileges before allowing
                if self.game.is_wizard(self.user.name()):
                    self.write(self.game.get_profiling_report())
                    return True

            if cmd == "escape":
                if self.input_redirect != None:
                    self.input_redirect = None
                    self.write("Successfully escaped from the redirect. ")
                else:
                    self.write("You cannot escape from a redirect, as there is none.")
                return True

            if cmd == 'auto-attack':
                self.user.auto_attack = True if self.user.auto_attack == False else False
                self.write("Auto attack toggled to %s." % self.user.auto_attack)
                return True
            
            if cmd == 'change':
                if self.words[1] == 'password':
                    self.write("Please enter your new --#password:")
                    self.input_redirect = self
                    self.changing_passwords = True
                    return True
            
            if cmd == 'upload':
                if self.game.is_wizard(self.user.name()):
                    allow_edits = self.game.get_edit_privileges(self.user.name(), path)
                    if allow_edits:
                        self.uploading_filename = path if os.path.basename(path) else ''  # returns '' if path doesn't end with a filename
                        self.write('Please select a file to --#upload:')
                    else:
                        self.write('You do not have permission to write to this directory.')
                    return True

            if cmd == 'download':
                if self.game.is_wizard(self.user.name()):
                    self.download_file(path)
                    return True
            
            if cmd == 'edit':
                # allowed = False
                # for (pop file/dirs off path)
                if self.game.is_wizard(self.user.name()):
                    allow_edits = self.game.get_edit_privileges(self.user.name(), path)
                    if allow_edits:
                        self.upload_confirm = False
                        self.download_file(path, edit_flag=True)
                    else:
                        self.write('You do not have permission to write to this directory.')
                    return True
            
            if cmd in ['vi', 'vim']:
                if self.game.is_wizard(self.user.name()):
                    allow_edits = self.game.get_edit_privileges(self.user.name(), path)
                    if allow_edits:
                        self.upload_confirm = False
                        self.download_file(path, edit_flag="vim")
                    else:
                        self.write('You do not have permission to write to this directory.')
                    return True
            
            if cmd == 'cd':
                if self.game.is_wizard(self.user.name()):  
                    if not arg:   # no dir given -> go to home dir
                        path = gametools.expandGameDir('~', player=self.user.name())
                    allow_reads = self.game.get_read_privileges(self.user.name(), path)
                    if allow_reads:
                        if os.path.exists(gametools.realDir(path)):
                            self.current_directory = path
                            self.write("Current directory now %s" % path)
                        else:
                            self.write('Error! No such file or directory.')
                    else:
                        self.write('You do not have permission to view this directory.')
                    return True

            if self.game.is_wizard(self.user.name()) and (cmd in ['ls', 'dir', 'cat', 'mkdir', 'rm', 'rmdir', 'mv', 'cp', 'pwd'] or self.try_all_console_commands):
                try:
                    if cmd == 'ls' and  platform.system() == "Linux":
                            self.words = ['ls', '--hide', '"__pycache__"'] + self.words[1:]
                    process = subprocess.run(shlex.split(" ".join(self.words)), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=0.5, cwd=gametools.realDir(self.current_directory), shell=False)
                    syntax_hilite = '```python\n' if cmd == 'cat' else '```\n'
                    self.write(syntax_hilite + str(process.stdout, "utf-8") + '\n```\n')
                    self.write(str(process.stderr, "utf-8"))
                    return True
                except Exception:
                    print(traceback.format_exc())
            
            game_file_cmds = {'savegame':self.game.save_game,
                         'loadgame':self.game.load_game}
            if cmd in game_file_cmds:
                if (len(self.words) == 2):
                    filename = self.words[1]
                    game_file_cmds[cmd](filename)
                else:
                    self.write("Usage: %s [filename]" % cmd)
                return True
            if cmd == 'save':
                if (len(self.words) == 2):
                    filename = self.words[1]
                    self.game.save_player(filename, self.user)
                else:
                    self.write("Usage: save [filename]")
                return True
            if cmd == 'load':
                if (len(self.words) == 2):
                    filename = self.words[1]
                    try:
                        self.game.load_player(filename, self.user, self)
                    except gametools.PlayerLoadError:
                        self.write("Encountered an error trying to load from file.")
                else:
                    self.write("Usage: load [filename]")
                return True
            if cmd == 'quit':
                self.user.emit("&nD%s fades from view, as if by sorcery...you sense that &p%s is no longer of this world." % (self.user.id, self.user.id))
                self.user.perceive("Saving...")
                self.save_and_backup(quit_behavior=True)
                self.write("--#quit")
                if len(self.words) > 1 and self.words[1] == 'game' and self.game.is_wizard(self.user.name()):
                    self.game.shutdown_console = self
                    self.game.keep_going = False
                self.user.detach()
                return True

        return False
    
    def upload_file(self, file, confirm_r=True):
        if self.confirming_replace:
            return
        if not self.uploading_filename:
            full_filename = os.path.join(self.current_directory, self.filename_input)
            self.uploading_filename = full_filename

        replacing_file = True
        try:
            f = open(gametools.realDir(self.uploading_filename, player=self.user.name()), 'r')
            try:
                self.user.log.debug('Found a file. Contents: %s' % f.read())
            except UnicodeDecodeError:
                self.user.log.error('This file is in the wrong format.')
            f.close()
        except FileNotFoundError:
            replacing_file = False
        except Exception as e:
            self.log.exception("Unable to write this file.")
        
        if not replacing_file or not confirm_r:
            self.user.log.debug('Decided to write file.')
            if platform.system() != 'Windows' and b'\r\n' in file:
                file = file.replace(b'\r\n', b'\n') 
            try:
                f = open(gametools.realDir(self.uploading_filename, player=self.user.name()), 'wb')
                f.write(file)
                f.close()
                self.write('Sucessfully uploaded file.')
                success = True
            except Exception as e:
                self.user.log.exception('Error writing file %s:' % gametools.realDir(self.uploading_filename, player=self.user.name()))
                success = False
            self.file_input = bytes()
            self.filename_input = ""
            self.upload_confirm = True
            if success:
                try:
                    r = requests.post("http://127.0.0.1:6553", data={"filepath":gametools.realDir(self.uploading_filename, player=self.user.name()), "commitmsg":"%s uploaded file %s" % (self.user.name(), self.uploading_filename)})
                    self.write(r.text)
                except:
                    self.user.log.warning("Gitbot failed to accept POST request")
                    self.user.log.debug(traceback.format_exc())
            self.uploading_filename = ""
        else:
            self.write('A file named %s already exits. Would you like to replace it with the new version you\'ve uploaded? Y/n:' % (self.uploading_filename))
            self.confirming_replace = True
            self.input_redirect = self

    def download_file(self, filename, edit_flag=False):
        if not filename:
            self.write("Error: no file specified to download.")
            return
        try:
            f = open(gametools.realDir(filename, player=self.user.name()), 'rb')
        except FileNotFoundError:
            if edit_flag:
                f = open(gametools.realDir(filename, player=self.user.name()), 'x')
                f.close()
                f = open(gametools.realDir(filename, player=self.user.name()), 'rb')
            else:
                self.write("Couldn't find a file named %s." % filename)
                return

        self.file_output = f.read()
        asyncio.ensure_future(connections_websock.file_send(self, edit_flag=edit_flag, filename=filename))
        f.close()
        self.write('%s file %s...' % ('Downloading' if not edit_flag else 'Opening', filename))

    def sanitizeHTML(self, html):
        return html.replace('<', '«').replace('>', '»')
    
    def choose_measurements(self, text):
        text = text.replace('[', '||[')
        text = text.replace(']', ']||')
        split_text = text.split('||')

        in_measurement = False
        correct_measurement = False
        to_continue = False

        new_text = ''

        for i in split_text:
            for j in Console.measurement_systems:
                if i == '['+j+']':
                    in_measurement = True
                    to_continue = True
                    if j == self.measurement_system:
                        correct_measurement = True
                    else:
                        correct_measurement = False
                elif i == '[/'+j+']':
                    in_measurement = False
                    to_continue = True
                    if j == self.measurement_system:
                        correct_measurement = True
                    else:
                        correct_measurement = False
            if to_continue:
                to_continue = False
                continue
            if (not in_measurement) or correct_measurement:
                new_text += i
        
        return new_text

    def write(self, text, indent=0):
        self.raw_output += str(text) + '\n'
        self.raw_output = self.choose_measurements(self.raw_output)
        self.raw_output = self.sanitizeHTML(self.raw_output)
        #self.raw_output = self.raw_output.replace('\t', '&nbsp&nbsp&nbsp&nbsp')
        asyncio.ensure_future(connections_websock.ws_send(self))

    def request_input(self, dest):
        self.input_redirect = dest
        self.user.log.info("Input from console %s given to %s!" % (self, dest))
    
    def console_recv(self, command):
        """Temporarily recieve information as a two-part command, e.g. changing passwords."""
        if self.changing_passwords:
            self.user.password = command
            self.changing_passwords = False
            self.input_redirect = None
        elif self.confirming_replace:
            if command in ['yes','y','Y','Yes','YES']:
                self.input_redirect = None
                self.confirming_replace = False
                self.upload_file(self.file_input, False)
            else:
                self.write('Okay, keeping old file.')
                self.input_redirect = None
                self.confirming_replace = False
                self.file_input = bytes()
    
    def get_next_input(self):
        """Get the next input from self.player_commands, removing it 
        from the list. Return None if self.player_commands is empty."""
        if not len(self.player_commands):
            return None
        next_input = self.player_commands[0]
        del self.player_commands[0]
        return next_input
    
    def handle_input(self):
        """Handle all input to the console. If the console is in a login state, 
        then call the _handle_login function with the given input. Otherwise, 
        check if the console can handle the command internally and add all remaining
        commands to the player_commands for the player to read from."""
        # if the login state is set to exit, the console is being deactivated, so we return without rescheduling
        if self.login_state == "EXIT":
            return

        # schedule the next occurance of handle_input
        self.game.schedule_event(0.2, self.handle_input)

        # check for uploaded files
        if self.file_input:
            self.upload_file(self.file_input, self.upload_confirm)

        # check to see if the user has sent any text 
        if (self.raw_input == ''):
            return
        (self.command, sep, self.raw_input) = self.raw_input.partition('\n')
        self.words = self.command.split()

        # if a user is in the login state, handle login until they have sucessfully connected
        if self.login_state:
            self._handle_login(self.command)
            return

        # if user types a console command, handle it and start over unless the player that called this is deactive
        internal = self._handle_console_commands()
        if not internal:
            if self.input_redirect != None:
                try:
                    self.input_redirect.console_recv(self.command)
                except AttributeError:
                    self.user.log.error('Error! Input redirect is not valid!')
                    self.input_redirect = None
            else:
                self.player_commands.append(self._replace_aliases())
        
 