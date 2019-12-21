import asyncio
import subprocess
import connections_websock
import secrets
import os
import re
import platform
import traceback

from debug import dbg
from parse import Parser
from player import Player
import gametools

class Console:
    default_width = 80
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
               Type 'quit' to save your progress and leave 
               the game."""

    def __init__(self, net_conn, game = None, encode_str='88838_defaultencodestr_9yq9h'):
        self.game = game
        self.user = None
        self.username = None
        self.raw_input = ''
        self.raw_output = ''
        self.file_input = bytes()
        self.filename_input = ''
        self.file_output = bytes()
        self.uploading_filename = ''
        self.current_directory = 'domains'
        self.change_players = False
        self.connection = net_conn
        self.input_redirect = None
        self.width = Console.default_width
        self.measurement_system = Console.default_measurement_system
        self.encode_str = str(encode_str)
        self.changing_passwords = False
        self.removing_directory = False
        self.confirming_replace = False
        self.alias_map = {'n':       'go north',
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
        self.legal_tags = {'span':     ['style'],
                           'div':      ['style'],
                           'b':        ['style'],
                           'br':       ['style'],
                           'code':     ['code'],
                           'dl':       ['style'],
                           'dd':       ['style'],
                           'dt':       ['style'],
                           'del':      ['style'],
                           'em':       ['style'],
                           'h1':       ['style'],
                           'h2':       ['style'],
                           'h3':       ['style'],
                           'h4':       ['style'],
                           'h5':       ['style'],
                           'h6':       ['style'],
                           'hr':       ['style'],
                           'i':        ['style'],
                           'ins':      ['style'],
                           'li':       ['style', 'value'],
                           'mark':     ['style'],
                           'meter':    ['style', 'high', 'low', 'max', 'min', 'optimum', 'value'],
                           'ol':       ['style', 'start', 'reversed', 'type'],
                           'p':        ['style'],
                           'pre':      ['style'],
                           'progress': ['style', 'max', 'value'],
                           'q':        ['style'],
                           's':        ['style'],
                           'kbd':      ['style'],
                           'samp':     ['style'],
                           'small':    ['style'],
                           'strong':   ['style'],
                           'sub':      ['style'],
                           'sup':      ['style'],
                           'u':        ['style'],
                           'ul':       ['style']}
        self.empty_elements = ['br', 'hr']

    def detach(self, user):
        if self.user == user:
            self.user = None

    def set_width(self, w):
        self.width = w
    
    def get_width(self):
        return self.width
    
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
        replace_words = self.words 
        if replace_words[0] in self.alias_map:
            replace_words[0] = self.alias_map[replace_words[0]]
        return " ".join(replace_words)
    
    def _set_verbosity(self, level=-1):
        if level != -1:
            dbg.set_verbosity(level, self.user.id)
            return "Verbose debug output now %s, verbosity level %s." % ('on' if level else 'off', dbg.verbosity[self.user.id])
        if self.user.id not in dbg.verbosity or dbg.verbosity[self.user.id] == 0:
            dbg.set_verbosity(1, self.user.id)
            return "Verbose debug output now on, verbosity level %s." % dbg.verbosity[self.user.id]
        else:
            dbg.set_verbosity(0, self.user.id)
            return "Verbose debug output now off."

    def _handle_verbose(self):
        try:
            level = int(self.words[1])
        except IndexError:
            self.write(self._set_verbosity())
            return
        except ValueError:
            if self.words[1] == 'filter':
                try:
                    s = self.words[2:]
                    dbg.set_filter_strings(s, self.user.id)
                    self.write("Set verbose filter to '%s', debug strings containing '%s' will now be printed." % (s, s))                      
                except IndexError:
                    dbg.set_filter_strings(['&&&'], self.user.id)
                    self.write("Turned off verbose filter; debug messages will only print if they are below level %d." % dbg.verbosity)
                return
            self.write("Usage: verbose [level]\n    Toggles debug message verbosity on and off (level 1 or 0), or sets it to the optionally provided [level]")
            return
        self.write(self._set_verbosity(level))
    
    def _findPath(self, pathwords):
        path = ''
        cont_path = ''
        dot_idx = False
        for i in pathwords:
            path += i+' '
        path = path[:-1]
        if path.startswith("~"):
            path = path.replace("~", "/home/%s" % self.user.names[0])
        if '..' in path: #TODO: Handle multiple '..' correctly
            num_back = path.count('..')
            dirlist = self.current_directory.split('/')[0:-num_back]
            for j in dirlist:
                cont_path += j+'/'
            path = path.replace('..','')
            dot_idx = True
        elif self.current_directory == '.':
            cont_path = ''
        else:
            cont_path = self.current_directory+'/'
        path = path.replace('\\','/')
        if path.startswith('/') and not dot_idx:
            path = path[1:]
            cont_path = ''
        path = cont_path + path
        path = path.replace('//','/')
        if path.endswith('/'):
            path = path[:-1]
        if path == '':
            path = '.'
        return path
    
    def _handle_console_commands(self):
        """Handle any commands internal to the console, returning True if the command string was handled."""
        if len(self.words) > 0:
            cmd = self.words[0]
            if cmd == 'alias':
                self._add_alias(self.command)
                return True
            
            if cmd == 'units':
                self._change_units(self.command)
                return True
            
            if cmd == 'help':
                self.write(self.help_msg)
                return True

            if cmd == 'debug':
                # check wizard privilages before allowing
                if self.user.wprivilages:
                    self.game.handle_exceptions = not self.game.handle_exceptions
                    self.write("Toggle debug exception handling to %s" % ("on" if self.game.handle_exceptions else "off"))
                    return True
                else:
                    self.write("You do not have permission to change the game's debug mode. If you would like to report a bug, type \"bug\" instead.")
                    return True
            
            if cmd == 'verbose':
                # check wizard privilages before allowing
                if self.user.wprivilages:
                    self._handle_verbose()
                    return True
                else:
                    self.write("Type \"terse\" to print short descriptions when entering a room.")
                    return True
            
            if cmd == 'profile':
                # check wizard privilages before allowing
                if self.user.wprivilages:
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
                    self.write("Please enter your new #password:")
                    self.input_redirect = self
                    self.changing_passwords = True
                    return True
            
            if cmd == 'upload':
                if self.user.wprivilages:
                    allow_edits = False
                    try:
                        for i in self.game.player_edit_privilages[self.user.names[0]]:
                            if re.fullmatch(i, self.current_directory):
                                allow_edits = True
                                break
                    except KeyError:
                        pass
                    if allow_edits:
                        if len(self.words) > 1 and self.words[1]:
                            self.uploading_filename = self.words[1] #TODO: make sure this is a valid filename
                        else:
                            self.uploading_filename = self.filename_input
                        if '.' not in self.uploading_filename:
                            self.uploading_filename += '.py'
                        self.write('Please select a file to #upload:')
                    else:
                        self.write('You do not have permission to write to this directory.')
                    return True

            if cmd == 'download':
                if self.user.wprivilages:
                    self.download_file(self.words[1:])
                    return True
            
            if cmd == 'cd':
                if self.user.wprivilages:
                    path = self._findPath(self.words[1:])
                    allow_reads = False
                    if path == '.':
                        allow_reads = True
                    try:
                        for i in self.game.player_read_privilages[self.user.names[0]]:
                            if re.fullmatch(i,path):
                                allow_reads = True
                                break
                    except KeyError:
                        pass
                    if allow_reads:
                        if os.path.exists(path):
                            self.current_directory = path
                        else:
                            self.write('Error! No such file or directory.')
                    else:
                        self.write('You do not have permission to view this directory.')
                    return True

            if self.user.wprivilages and cmd in ['ls', 'cat', 'mkdir', 'rm', 'rmdir', 'mv', 'cp']:
                try:
                    process = subprocess.run(self.words, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=0.5, cwd=self.current_directory)
                    self.write(str(process.stdout, "utf-8"))
                    self.write(str(process.stderr, "utf-8"))
                    return True
                except Exception:
                    print(traceback.format_exc())
            '''
            if cmd == 'ls':
                if self.user.wprivilages:
                    ls_info = '<div style="column-count:4">'
                    try:
                        param = self.words[1]
                    except IndexError:
                        param = None
                    dirs, files = [[x[1],x[2]] for x in os.walk(self.current_directory)][0]
                    for d in dirs:
                        if (not d.startswith('.') and d != '__pycache__') or param == '-a':
                            ls_info += d+' '
                    for f in files:
                        if not f.startswith('.') or param == '-a':
                            ls_info += f+' '
                    ls_info += '</div>'
                    self.write(ls_info)
                    return True
            
            if cmd == 'cat':
                if self.user.wprivilages:
                    if len(self.words) > 1:
                        filename = self.words[1] #TODO: make sure this is a valid filename
                        try:
                            f = open(self.current_directory+'/'+filename, 'r')
                            self.write(f.read())
                            f.close()
                        except FileNotFoundError:
                            self.write('Error! No file named %s.' % filename)
                        return True
            
            if cmd == 'mv':
                if self.user.wprivilages:
                    if len(self.words) > 2:
                        filenames = self.words[1:-1]
                        dest = self.words[-1]

                        dest_path = self._findPath([dest])
                        allow_edits = False
                        allow_dest_edits = False
                        try:
                            for i in self.game.player_edit_privilages[self.user.names[0]]:
                                if re.fullmatch(i, self.current_directory):
                                    allow_edits = True
                                if re.fullmatch(i, dest_path):
                                    allow_dest_edits = True
                        except KeyError:
                            pass

                        if allow_dest_edits and allow_edits:
                            if '.' not in dest_path.split('/')[-1]:
                                for i in filenames:
                                    if os.path.exists(self.current_directory+'/'+i):
                                        os.replace(self.current_directory+'/'+i, dest_path+'/'+i)
                                        add_return = subprocess.run(["git","add","-A"])
                                        commit_return = subprocess.run(["git","commit","-m","%s moved file %s" % (self.user.names[0], i)])
                                    else:
                                        self.write('Error, no file named %s.' % i)
                            else:
                                if len(self.words) == 3:
                                    if os.path.exists(self.current_directory+'/'+filenames[0]):
                                        os.replace(self.current_directory+'/'+filenames[0], dest_path)
                                        add_return = subprocess.run(["git","add","-A"])
                                        commit_return = subprocess.run(["git","commit","-m","%s renamed file %s" % (self.user.names[0], filenames[0])])
                                    else:
                                        self.write('Error, no file named %s.' % filenames[0])
                                else:
                                    self.write('Error, input invalid.')
                        else:
                            self.write('You do not have permission to perform this action.')
                    else:
                        self.write('Usage: mv [src] [dest]')
                    return True
            
            if cmd == 'rm':
                if self.user.wprivilages:
                    allow_edits = False
                    try:
                        for i in self.game.player_edit_privilages[self.user.names[0]]:
                            if re.fullmatch(i, self.current_directory):
                                allow_edits = True
                                break 
                    except KeyError:
                        pass
                    if allow_edits:
                        if len(self.words) > 1:
                            filename = self.words[1]
                            if os.path.exists(self.current_directory+'/'+filename):
                                self.removing_directory = self.current_directory+'/'+filename
                                self.input_redirect = self
                                self.write('Are you sure you would like to complete this operation? Y/n:')
                            else:
                                self.write('Error, no file named %s exists.' % filename)
                        else:
                            self.write('What did you mean to remove?')
                    else:
                        self.write('You do not have permission to remove files from this directory.')
                    return True
            
            if cmd == 'mkdir':
                if self.user.wprivilages:
                    if len(self.words) > 1:
                        filename = self.words[1]
                        if not os.path.exists(self.current_directory+'/'+filename):
                            os.mkdir(self.current_directory+'/'+filename)
                        else:
                            self.write('Error, A directory named %s already exits!' % filename)
                    else:
                        self.write('mkdir requires a directory name')
                    return True
            
            if cmd == 'rmdir':
                if self.user.wprivilages:
                    if len(self.words) > 1:
                        filename = self.words[1]
                        try:
                            os.rmdir(self.current_directory+'/'+filename)
                        except FileNotFoundError:
                            self.write('Error, no directory named %s exits.' % filename)
                        except OSError:
                            self.write('Error, only empty directories may be removed.')
                    return True'''
            
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
                self.user.emit("&nD%s fades from view, as if by sorcery...you sense that &p%s is no longer of this world." % (self.user, self.user))
                self.game.save_player(os.path.join(gametools.PLAYER_DIR, self.user.names[0]), self.user)
                self.game.create_backups(os.path.join(gametools.PLAYER_BACKUP_DIR, self.user.names[0]), self.user, os.path.join(gametools.PLAYER_DIR, self.user.names[0]))
                self.write("#quit")
                if len(self.words) > 1 and self.words[1] == 'game' and self.user.wprivilages:
                    self.game.shutdown_console = self
                    self.game.keep_going = False
                return "__quit__"

        return False
    
    def upload_file(self, file, confirm_r=True):
        if self.confirming_replace:
            return
        replacing_file = True
        try:
            f = open(self.current_directory+'/'+self.uploading_filename, 'r')
            dbg.debug('Found a file. Contents: %s' % f.read(), 2)
            f.close()
        except FileNotFoundError:
            replacing_file = False
        
        if not replacing_file or not confirm_r:
            dbg.debug('Decided to write file.', 2)
            if platform.system() != 'Windows' and b'\r\n' in file:
                file = file.replace(b'\r\n', b'\n') 
            f = open(self.current_directory+'/'+self.uploading_filename, 'wb')
            f.write(file)
            f.close()
            self.write('Sucessfully uploaded file.')
            self.file_input = bytes()
            add_return = subprocess.run(["git","add","-A"])
            commit_return = subprocess.run(["git","commit","-m","%s uploaded file %s" % (self.user.names[0], self.uploading_filename)])
        else:
            self.write('A file named %s already exits. Would you like to replace it with the new version you\'ve uploaded? Y/n:' % (self.current_directory+'/'+self.uploading_filename))
            self.confirming_replace = True
            self.input_redirect = self

    def download_file(self, filename_words):
        filename = ''
        for x in filename_words:
            filename += x

        try:
            f = open(self.current_directory+'/'+filename, 'rb')
        except FileNotFoundError:
            self.write("Couldn't find a file named %s." % filename)
            return

        self.file_output = f.read()
        asyncio.ensure_future(connections_websock.file_send(self))
        f.close()
        self.write('Downloading file %s...' % filename)

    def sanitizeHTML(self, html):
        return html.replace('<', '«').replace('>', '»')
    
    def choose_measurements(self, text):
        text = text.replace('[', '|[')
        text = text.replace(']', ']|')
        split_text = text.split('|')

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
        dbg.debug("Input from console %s given to %s!" % (self, dest), 2)
    
    def console_recv(self, command):
        """Temporarily recieve information as a two-part command, e.g. changing passwords."""
        if self.changing_passwords:
            self.user.password = command
            self.changing_passwords = False
            self.input_redirect = None
        elif self.removing_directory:
            if command in ['yes','y','Y','Yes','YES']:
                os.remove(self.removing_directory)
                add_return = subprocess.run(['git','add','-A'])
                commit_return = subprocess.run(['git','commit','-m','%s removed file %s.' % (self.user.names[0], self.removing_directory)])
                self.removing_directory = False
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
            self.upload_file(self.file_input)
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
                dbg.debug('Error! Input redirect is not valid!')
                self.input_redirect = None
        # replace any aliases with their completed version
        self.final_command = self._replace_aliases()
        return self.final_command

# This is the end of file
