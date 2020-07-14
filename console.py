import asyncio
import functools
import subprocess
import json
import sys
import time

import gametools

# default location of saved console attributes file
RC_PATH = "home/"  # note this is a relative path
RC_NAME = ".consolerc"

usernames_open = []

class GameserverCommunicationProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
    
    def connection_lost(self, exc):
        # TODO: Deal with unexpected closures
        value = super().connection_lost(exc)
        if self.cons.disconnecting_state:
            self.cons.write_output("Disconnected from gameserver.")
            self.cons.loop.stop()
        return value
    
    def data_received(self, data):
        #print(data.decode('utf-8'))
        data = data.decode('utf-8')
        splitData = data.split('\u0004')
        for splitDatum in splitData:
            if splitDatum != '':
                self.cons.receive_from_gameserver(splitDatum)
    
    def send_message(self, message):
        self.transport.write(message.encode('utf-8'))

class BaseConsole:
    """A base class for all game consoles, containing the basic code to
    communicate with the game server and to run shell commands. Subclasses
    provide more functionality."""
    saved_attributes = ["current_player_name"] # attributes that the console should save in its config file
        measurement_systems = ['IMP', 'SI']
    default_measurement_system = 'IMP'
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
    def __init__(self, username, gameserver_host, gameserver_port):
        self.username = username
        self.loop = asyncio.get_event_loop()
        # items related to connection to gameserver
        self.protocol = None
        self.connect_to_gameserver(gameserver_host, gameserver_port)
        self.gameserver_input = []
        self.gameserver_output = []
        # items related to bash shell integration
        self.bash_output = b''
        self.bash_input = ''
        self.shell_mode = False
        self.loop.run_until_complete(self._setup_bash_console())
        # user input information (subclasses provide more functionality)
        self.current_string = ''
        # user customizations
        self.measurement_system = BaseConsole.default_measurement_system
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
        # player save/load information
        self.current_player_name = None
        self.player_loaded = False
        # start the console
        self.disconnecting_state = False # disconnect on connection close
        self.startup_console()
    
    def wizard_privilages(self):
        return 'wizard' in subprocess.run('groups', stdout=subprocess.PIPE).stdout
    
    #
    # Functions related to console startup and shutdown
    #

    def startup_console(self):
        """Start the asyncio event loop, first loading saved attributes
        (such as player name, and eventually aliases etc). When the loop
        exits, save those attributes again."""
        print('starting console...')
        try:
            if self.username:
                f = open(RC_PATH + f"{self.username}" +"/" + RC_NAME)
                attrs_json = f.read()
                f.close()
                attrs_dict = json.loads(attrs_json)
                for i in list(attrs_dict):
                    if i in self.saved_attributes:
                        self.__dict__[i] = attrs_dict[i]
        except Exception as e:
            print(e, file=sys.stderr)

        print('starting loop...')
        self.loop.call_later(30, self.autosave)
        #self.loop.call_later(2, self._call_await_bash_setup)
        self.loop.call_later(1, self.call_read_input)
        self.loop.run_forever()

        # Console has disconnected, clean up

        print('shutting down console...')
        try:
            if self.username:
                f = open(RC_PATH + f"{self.username}" +"/" + RC_NAME, "w")
                attrs_dict = {}
                for i in list(self.saved_attributes):
                    if i in self.__dict__:
                        attrs_dict[i] = self.__dict__[i]
                attrs_json = json.dumps(attrs_dict)
                f.write(attrs_json)
                f.close()
        except Exception as e:
            print(e, file=sys.stderr)
    
    #
    # Functions for connecting to the gameserver
    #

    def connect_to_gameserver(self, address, port, retry_num=10, delay=2):
        """Create a connection to the gameserver, setting `self.protocol`."""
        for i in range(0, retry_num):
            try:
                transport, protocol = self.loop.run_until_complete(self.loop.create_connection(GameserverCommunicationProtocol, host=address, port=port))
                self.protocol = protocol
                self.protocol.cons = self
                break
            except ConnectionRefusedError:
                print(f"Connection refused; retrying in {delay} seconds...", file=sys.stderr)
                time.sleep(delay)
                delay *= 2
                continue
    
    def receive_from_gameserver(self, message_json):
        """Receive a message from the gameserver. This function 
        should parse the message dictionary and decide what action
        to take. This implementation is very basic and can be subclassed
        for more functionality."""
        try:
            message_dict = json.loads(message_json)
        except Exception as e:
            self.write_output("Error unpacking JSON message from server! Error: \n", e)
            return
        
        try:
            message_type = message_dict['type']
        except KeyError:
            self.write_output("Invalid message dictionary: no `type`")
            return
        
        if message_type == 'response':
            try:
                message_str = message_dict['message']
                self.write_output(message_str)
            except KeyError:
                self.write_output("Invalid message dictionary: `type` was set to `response` but no `message` found")
                return
        
        elif message_type == 'error':
            try:
                message_str = message_dict['message']
                error_code = message_dict['error_code']
                self.write_output("An error occurred in the request.")
                self.write_output(f"Error code: {error_code} ({gametools.console_error_codes[error_code]['name']})")
                self.write_output(f"Error message: {message_str}")
            except KeyError:
                self.write_output("An error occurred trying to report an error! Please report another error.")
                return
        
        elif message_type == 'save_return':
            try:
                player_json = message_dict['player_json']
            except KeyError:
                self.write_output("Error: `type` set to `save_return` but `player_json` missing")
                return
            try:
                self._save_player_to_file(player_json, self.current_player_name)
            except Exception as e:
                self.write_output("An error occurred while saving the player. Printing below: \n"+e)
                return
        
        elif message_type == 'load_status':
            try:
                self.player_loaded = bool(int(message_dict['status']))
            except KeyError:
                self.write_output("Error: `type` set to `load_status` but `status` missing")
                return
            except Exception as e:
                self.write_output("An error occured trying to change the load status. Printing below \n"+e)
            
        else:
            self.write_output(f"The message type is not supported. Message type: {message_type}")

    def send_to_gameserver(self, type, message=None, player_json=None, player_name=None):
        """Send a message to the gameserver with the given attributes."""
        message_dict = {
            "type": type
        }
        if message:
            message_dict["message"] = message
        if player_json:
            message_dict["player_json"] = player_json
        if player_name:
            message_dict['player_name'] = player_name
        try:
            message_json = json.dumps(message_dict)+'\u0004' # separate messages by this character
        except Exception as e:
            self.write_output("An error occurred preparing the message for the gameserver. Error message: "+e)
            return
        self.protocol.send_message(message_json)
    
    def autosave(self):
        """Send a periodic save request every 30 seconds."""
        print('autosave called')
        if self.player_loaded:
            self.send_to_gameserver('save')
        self.loop.call_later(30, self.autosave)
    
    #
    # Functions for running commands in the bash subprocess
    #
    
    async def _setup_bash_console(self):
        """Create the bash process, and begin reading and writing from it."""
        self.bash_process = await asyncio.create_subprocess_exec('bash', stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        
    async def _await_bash_setup(self):
        await asyncio.gather(self._read_bash_stderr(self.bash_process.stderr), self._read_bash_stdout(self.bash_process.stdout), self._write_bash_stdin(self.bash_process.stdin))
    
    def _call_await_bash_setup(self):
        asyncio.ensure_future(self._await_bash_setup())
    
    async def _read_bash_stderr(self, stderr):
        """Read the stderr of the bash process."""
        while True:
            print('starting bash read')
            buf = await stderr.read()
            print('read something')
            if not buf:
                break
            self.bash_output += buf

    async def _read_bash_stdout(self, stdout):
        """Read the stdout of the bash process."""
        while True:
            print('starting bash read')
            buf = await stdout.read()
            print('read something')
            if not buf:
                break
            self.bash_output += buf
    
    async def _write_bash_stdin(self, stdin):
        """Write the stdin of the bash process."""
        while True:
            if self.bash_input:
                buf = f'{self.bash_input}\n'.encode('utf-8')
                stdin.write(buf)
                await stdin.drain()
                if self.bash_input == 'exit':
                    break
    
    async def _write_bash_output(self):
        """Collect the bash output and write it to the console."""
        final_output_str = ""
        while True:
            bash_output_str = self.bash_output.decode('utf-8')
            if '\n' in bash_output_str:
                output_str, sep, remaining_str = bash_output_str.partition('\n')
                self.bash_output = remaining_str.encode('utf-8')
                final_output_str += output_str
            else:
                break
        self.loop.call_later(0.1, functools.partial(self.write_output, final_output_str))
    
    def run_bash_command(self, command):
        """Run a bash command, printing the returned value to the console when ready."""
        self.bash_input = command
        self.loop.run_until_complete(self._write_bash_output())
    
    #
    # Input / Output functions (for subclassing)
    #

    def _load_player_from_file(self, input_words, player_name):
        """Load a player save file, returning True if an error occurred."""
        try:
            f = open(f"saved_players/{player_name}.OADplayer", 'r')
            player_json = f.read()
            f.close()
            self.current_player_name = player_name
            self.send_to_gameserver('load', player_json=player_json)
            return False
        except FileNotFoundError:
            self.write_output(f"No player named {player_name} found. To create a new player, type 'create {player_name}")
        except PermissionError:
            self.write_output(f"The player {player_name} is not yours. Please try again.")
        except Exception as e:
            self.write_output(e)
        return True

    def _save_player_to_file(self, player_json, player_name):
        """Load a player save file, returning True if an error occurred."""
        try:
            f = open(f"saved_players/{player_name}.OADplayer", 'w')
            f.write(player_json)
            f.close()
            return False
        except FileNotFoundError:
            self.write_output(f"No player named {player_name} found. To create a new player, type 'create {player_name}")
        except PermissionError:
            self.write_output(f"The player {player_name} is not yours. Please try again.")
        except Exception as e:
            self.write_output(e)
        return True
    def _add_alias(self, input_str, words):
        instructions = 'To create a new alias, type:\n    alias [a] [text]\n' \
                        'where [a] is the new alias and [text] is what will replace the alias.'
         
        if len(words) == 1:
            # print a list of current aliases & instructions for adding
            self.write_output('Current aliases:')
            for a in sorted(self.alias_map, key=self.alias_map.get):
                self.write_output('%s = %s' % (a.rjust(12), self.alias_map[a]))
            self.write_output(instructions)
            return 
        alias = words[1]
        if len(words) == 2:
            # print the particular alias if it exists
            if (alias in self.alias_map):
                self.write_output("'%s' is currently aliased to '%s'" % (alias, self.alias_map[alias]))
            else:
                self.write_output("'%s' is not currently aliased to anything." % alias)
                self.write_output(instructions)
            return 
        # new alias specified, insert it into the alias_map
        if (alias in self.alias_map):
            self.write_output("'%s' is currently aliased to '%s'; changing." % (alias, self.alias_map[alias]))
        expansion = input_str.split(maxsplit=2)[2]    # split off first two words and keep the rest
        self.alias_map[alias] = expansion
        self.write_output("'%s' is now an alias for '%s'" % (alias, expansion))
        return
    
    def _change_units(self, cmd):
        cmd = cmd.split(' ')
        if len(cmd) == 2:
            if cmd[1].upper() in self.measurement_systems:
                self.measurement_system = cmd[1].upper()
                self.write_output('Changed units to %s.' % self.measurement_system)
            else:
                self.write_output('Not an accepted measurement system. Accepted ones are:\n' + [x for x in self.measurement_systems])
        else:
            self.write_output('Current units are: %s\nType units [system] to change them.' % self.measurement_system)

    def _replace_aliases(self, words):
        if not words:  # Return if there are no words to replace with aliases
            return
        replace_words = words
        if replace_words[0] in self.alias_map:
            replace_words[0] = self.alias_map[replace_words[0]]
        return " ".join(replace_words)
  
    def handle_command(self, input_str, additional_cmds_map={}):
        """Decide what to do with a user command: 
        - pass to gameserver,
        - pass to shell, or
        - save and load a player."""
        if len(input_str) == 0: # nothing typed
            return
        #print("handling", input_str)
        input_words = input_str.lower().split(" ")
        if input_words[0] == "load":
            usage = "Please type `load <name>` to specify a name for your "
            "character, or to load a new character.  Names must be "
            "a single word with no spaces."
            if len(input_words) == 1:
                if self.current_player_name:
                    player_name = self.current_player_name
                else:
                    self.write_output(usage)
                    return
            elif len(input_words) == 2:
                player_name = input_words[1]
            else:
                self.write_output(usage)
                return
            if self.player_loaded:
                self.send_to_gameserver('save')
            if self._load_player_from_file(input_words, player_name):
                return

        elif input_words[0] == "create":
            usage = "Please type `create <name>` to create a player named "
            "<name>. Names must be a single word with no spaces."
            if len(input_words) == 1:
                self.write_output(usage)
                return
            elif len(input_words) == 2:
                player_name = input_words[1]
            else:
                self.write_output(usage)
                return
            if self.player_loaded:
                self.send_to_gameserver('save')
            try:
                playerFile = open(f'saved_players/{player_name}.OADplayer', 'r')
            except FileNotFoundError:
                # player does not exist, can create safely
                playerFile = open(f'saved_players/{player_name}.OADplayer', 'w')
                self.send_to_gameserver('create', player_name=player_name)
                self.current_player_name = player_name
                playerFile.close()
                self.send_to_gameserver('save')
                pass
            else:
                # player already exists
                self.write_output("That username already exists!")
                playerFile.close()

        elif input_words[0] == "save":
            usage = "Please type `save` to save your player."
            if not self.player_loaded and input_words != ['save', 'force']:
                self.write_output('No player is loaded. Type `load <name>` to load a player.')
                return
            if len(input_words) != 1:
                self.write_output(usage)
                return
            self.send_to_gameserver('save')
        
        elif input_words[0] in ["unload", "quit"]:
            usage = "Type `unload` to save and unload your player, or `quit` to save and quit."
            if len(input_words) != 1:
                self.write_output(usage)
                return
            if self.player_loaded:
                self.send_to_gameserver('save')
                self.send_to_gameserver('unload')
            elif input_words[0] == "unload":
                self.write_output("No player is loaded! Type `load <name>` to load a player.")
                return
            
            if input_words[0] == "quit":
                self.send_to_gameserver('disconnect')
                self.disconnecting_state = True
        
        elif input_words[0] in ["shell", "bash"]:
            if self.wizard_privilages():
                if len(input_words) == 1:
                    if input_words[0] != "bash":
                        self.shell_mode = not self.shell_mode
                    else:
                        if not self.shell_mode:
                            self.shell_mode = True
                elif len(input_words) == 2:
                    if input_words[1] in ["on", "active", "activate", "open", "start"]:
                        self.shell_mode = True
                    elif input_words[1] in ["off", "cancel", "close", "deactivate", "end"]:
                        self.shell_mode = False
                    elif input_words[1] in ["toggle", "change"]:
                        self.shell_mode = not self.shell_mode
                    elif input_words[0] != "bash" or not self.shell_mode:
                        self.write_output("This is not a valid shell mode. Please try again. _Hint: please turn shell mode on before typing bash command._")
            else:
                self.write_output("You do not have permission to perform this action.")

        elif input_words[0] == 'alias':
            self._add_alias(input_str, input_words)
            
        elif input_words[0] == 'units':
            self._change_units(input_str)
        
        elif input_words[0] == "help":
            self.write_output(self.help_msg)
            
        elif input_words[0] in list(additional_cmds_map):
            try:
                additional_cmds_map[input_words[0]](input_str, input_words)
            except Exception as e:
                self.write_output(e)
                return
        elif self.shell_mode or input_words[0] in ['ls', 'cd', 'cat', 'mkdir', 'rm', 'rmdir', 'mv', 'cp', 'pwd']:
            if self.wizard_privilages:
                self.run_bash_command(input_str)
            else:
                self.write_output("You do not have permission to perform this action.")
        else:
            if self.player_loaded:
                self.send_to_gameserver('parse', message=input_str)
            else:
                self.write_output("Please load a player before doing any actions.")
    
    def call_read_input(self):
        asyncio.ensure_future(self.read_input())

    def write_output(self, *output_strs):
        """Write the given output. Must be subclassed for additional functionality."""
        raise NotImplementedError("write_output must be subclassed")

    async def read_input(self):
        """Read the current input. Must be subclassed for additional functionality."""
        raise NotImplementedError("read_input must be subclassed")

class TextConsole(BaseConsole):
    """A very basic text-only console. Intended usage includes: testing. Intended usage excludes: everything else."""
    def write_output(self, *output_strs):
        print(*output_strs)
    
    async def read_input(self):
        while True:
            inp = input("> ")
            self.loop.call_later(0.01, functools.partial(self.handle_command, inp))
            await asyncio.sleep(1)

class WebclientConsole(BaseConsole):
    """A console that uses the game serving protocol to connect to a user's webclient. This is the main console that is used in the game."""
    pass