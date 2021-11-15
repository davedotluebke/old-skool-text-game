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
    measurement_systems = ['IMP', 'SI']
    default_measurement_system = 'IMP'
    prompt = "--> "
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
        self.raw_input = ''
        self.raw_output = ''
        self.file_input = bytes()
        self.filename_input = ''
        self.file_output = bytes()
        self.filename_output = ''
        self.uploading_filename = ''
        self.current_directory = '/domains'  # always in 'game directory space'
        self.change_players = False
        self.try_all_console_commands = False
        self.connection = net_conn
        self.input_redirect = None
        self.upload_confirm = True
        self.measurement_system = Console.default_measurement_system
        self.encode_str = str(encode_str)
        self.changing_passwords = False
        self.confirming_replace = False
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
                self.game.save_player(gametools.realDir(gametools.PLAYER_DIR, self.user.names[0]), self.user)
                self.game.create_backups(gametools.realDir(gametools.PLAYER_BACKUP_DIR, self.user.names[0]), self.user, gametools.realDir(gametools.PLAYER_DIR, self.user.names[0]))
                self.write("--#quit")
                if len(self.words) > 1 and self.words[1] == 'game' and self.game.is_wizard(self.user.name()):
                    self.game.shutdown_console = self
                    self.game.keep_going = False
                return "__quit__"

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

    def take_input(self):
        if self.file_input:
            self.upload_file(self.file_input, self.upload_confirm)
        if (self.raw_input == ''):
            return None
        (self.command, sep, self.raw_input) = self.raw_input.partition('\n')
        self.words = self.command.split()
        # if user types a console command, handle it and start over unless the player that called this is deactive
        internal = self._handle_console_commands()
        if internal == "__quit__":
            return "__quit__"
        if internal:
            return "__noparse__"
        if self.input_redirect != None:
            try:
                self.input_redirect.console_recv(self.command)
                return "__noparse__"
            except AttributeError:
                self.user.log.error('Error! Input redirect is not valid!')
                self.input_redirect = None
        # replace any aliases with their completed version
        self.final_command = self._replace_aliases()
        return self.final_command

