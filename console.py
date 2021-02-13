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
    saved_attributes = ["current_player_name", "measurement_system", "alias_map"] # attributes that the console should save in its config file
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
        self.GameserverProtocolVersion = [0, 1]
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
        self.auto_load_player = True
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
    
    def wizard_privilages(self):
        return self.username in subprocess.run(['getent', 'group', 'wizards'], stdout=subprocess.PIPE).stdout.decode('utf-8').split(":")[-1].strip().split(",")
    
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
        self.loop.call_later(2, self._call_await_bash_setup)
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
            "type": type,
            "version": self.GameserverProtocolVersion
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
        if self.player_loaded:
            self.send_to_gameserver('save')
        self.loop.call_later(30, self.autosave)
    
    #
    # Functions for running commands in the bash subprocess
    #
    
    async def _setup_bash_console(self):
        """Create the bash process, and begin reading and writing from it."""
        self.bash_process = await asyncio.create_subprocess_exec('/bin/bash', stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        
    async def _await_bash_setup(self):
        await asyncio.gather(self._read_bash_stderr(self.bash_process.stderr), self._read_bash_stdout(self.bash_process.stdout), self._write_bash_stdin(self.bash_process.stdin))
    
    def _call_await_bash_setup(self):
        asyncio.ensure_future(self._await_bash_setup())
    
    async def _read_bash_stderr(self, stderr):
        """Read the stderr of the bash process."""
        while True:
            buf = await stderr.read(1)
            if not buf:
                break
            self.bash_output += buf
            if buf == b'\n':
                final_output = self.bash_output.decode('utf-8')
                self.bash_output = b''
                self.loop.call_later(0.1, functools.partial(self.write_output, final_output))
            await asyncio.sleep(0)

    async def _read_bash_stdout(self, stdout):
        """Read the stdout of the bash process."""
        while True:
            buf = await stdout.read(1)
            if not buf:
                break
            self.bash_output += buf
            if buf == b'\n':
                final_output = self.bash_output.decode('utf-8')
                self.bash_output = b''
                self.loop.call_later(0.1, functools.partial(self.write_output, final_output))
            await asyncio.sleep(0)
    
    async def _write_bash_stdin(self, stdin):
        """Write the stdin of the bash process."""
        while True:
            if self.bash_input:
                buf = f'{self.bash_input}\n'.encode('utf-8')
                stdin.write(buf)
                await stdin.drain()
                if self.bash_input == 'exit':
                    break
                self.bash_input = ''
            await asyncio.sleep(0)
    
    def run_bash_command(self, command):
        """Run a bash command, printing the returned value to the console when ready."""
        self.bash_input = command
    
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
    
    def _create_player_from_file(self, player_name):
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
            for j in BaseConsole.measurement_systems:
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
    
  
    def handle_command(self, input_str, additional_cmds_map={}, call_on_quit=None):
        """Decide what to do with a user command: 
        - pass to gameserver,
        - pass to shell, or
        - save and load a player."""
        print("handle command called")
        if len(input_str) == 0: # nothing typed
            return
        input_words = input_str.lower().split(" ")
        print("input_words = ", input_words)
        print("self.wizard_privilages() = ", self.wizard_privilages())
        if input_words[0] == "load" and self.wizard_privilages():
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

        elif (input_words[0] == "create" and self.wizard_privilages()):
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
            self._create_player_from_file(player_name)

        elif input_words[0] == "save":
            print("User typed save")
            usage = "Please type `save` to save your player."
            if not self.player_loaded and input_words != ['save', 'force']:
                self.write_output('No player is loaded. Type `load <name>` to load a player.')
                return
            if len(input_words) != 1:
                self.write_output(usage)
                return
            self.send_to_gameserver('save')
        
        elif input_words[0] in ["unload", "quit"]:
            print("unload/quit called")
            usage = "Type `unload` to save and unload your player, or `quit` to save and quit."
            if len(input_words) != 1:
                self.write_output(usage)
                return
            if input_words[0] == "unload" and not self.wizard_privilages():
                self.write_output("You must have wizard privilages to unload. Try `quit` instead.")
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
                if call_on_quit:
                    call_on_quit()
        
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
            print("help called")
            self.write_output(self.help_msg)
        
        elif input_words[0] in ["password"] or (len(input_words) == 2 and input_words[0] == "change" and input_words[1] == "password"):
            self.write_output("Please enter a new password:", message_type="password_request")
        
        elif input_words[0] == "download":
            if self.wizard_privilages():
                if len(input_words) > 1:
                    self.download_file(input_str.partition(" ")[2])
            else:
                self.write_output("Wizard privilages are required to upload and download files.")

        elif input_words[0] == "edit":
            if self.wizard_privilages():
                if len(input_words) > 1:
                    self.download_file(input_str.partition(" ")[2], for_edit=True)
            else:
                self.write_output("Wizard privilages are required to upload and download files.")
        
        elif input_words[0] == "upload":
            if self.wizard_privilages():
                if len(input_words) > 1:
                    self.ws_protocol.send_message(json.dumps({
                        'type': 'upload_request',
                        'data': 'Please select a file to upload.'
                    }))
            else:
                self.write_output("Wizard privilages are required to upload and download files.")
        
        elif input_words[0] == "console" and self.wizard_privilages():
            usage = "Welcome to the advanced console management system! Possible commands are:\n" \
            "read/get [attr]: read self.[attr], printing its value\n" \
            "write/set [attr] [value]: write self.[attr], setting its value to [value]\n" \
            "execute/run [code]: run the code [code]"
            if len(input_words) == 1:
                self.write_output(usage)
                return
            if input_words[1] in ["read", "get"]:
                for i in input_words[2:]:
                    self.write_output(f"{i}: {eval(f'self.{i}')}")
            elif input_words[1] in ["write", "set"]:
                if len(input_words) != 4:
                    self.write_output("Usage: console [set] [attr] [value]")
                    return
                else:
                    exec(f"self.{input_words[3]} = {input_words[4]}")
                    self.write_output(f"{input_words[3]}: {input_words[4]}")
            elif input_words[1] in ["execute", "run"]:
                exec(input_str.split(" ", maxsplit=2)[2])
                    
        elif input_words[0] in list(additional_cmds_map):
            try:
                additional_cmds_map[input_words[0]](input_str, input_words)
            except Exception as e:
                self.write_output(e)
                return
        elif self.shell_mode or input_words[0] in ['ls', 'cd', 'cat', 'mkdir', 'rm', 'rmdir', 'mv', 'cp', 'pwd']:
            if self.wizard_privilages():
                self.run_bash_command(input_str)
            else:
                self.write_output("You do not have permission to perform this action.")
        else:
            if self.player_loaded:
                print("sending message to gameserver: %s" % input_str)
                # replace aliases with their full versions
                input_str = self._replace_aliases(input_str.split(" "))
                self.send_to_gameserver('parse', message=input_str)
            else:
                if not self.current_player_name and len(input_words) == 1 and self.auto_load_player:
                    print("creating player, name %s" % input_str)
                    self._create_player_from_file(input_words[0])
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

class WebclientCommunicationProtocol(asyncio.Protocol):
    """An interface for communicating with the webclient. 
    Note that this does not actually communicate directly 
    with the webclient, but instead with the Console Overseer, 
    which forwards the messages via its websocket server."""
    def connection_made(self, transport):
        self.transport = transport
    
    def connection_lost(self, exc):
        return super().connection_lost()
    
    def data_received(self, data):
        data = data.decode('utf-8')
        data_list = data.split('\u0004')
        for data_json in data_list:
            if not data_json:
                continue
            data_dict = json.loads(data_json)
            try:
                data_type = data_dict['type']
                data_str = data_dict['data'].strip()
                if data_type == "file":
                    data_filename = data_dict['filename']
            except KeyError:
                self.cons.write_output(f'The data_dict is missing a paramater! Paramaters are: {data_dict}')
                continue
            if data_type == "command":
                self.cons.handle_command(data_str)
            elif data_type == "file":
                self.cons.upload_file(data_str, data_filename)
            elif data_type == "connection_init":
                self.cons.init_connection(data_str)
            else:
                self.cons.write_output(f'The data type is invalid! Data type: {data_type}')
    
    def send_message(self, message_json):
        self.transport.write(message_json.encode('utf-8')+'\u0004'.encode('utf-8'))

class WebclientConsole(BaseConsole):
    """A console that uses the game serving protocol to connect to a user's webclient. This is the main console that is used in the game."""
    def __init__(self, username, gameserver_host, gameserver_port, ws_host, ws_port, connection_code):
        self.connection_code = connection_code
        self.WebclientProtocolVersion = [0, 1]
        super().__init__(username, gameserver_host, gameserver_port)
        self.connect_to_webclient(ws_host, ws_port)

    def connect_to_webclient(self, address, port, retry_num=10, delay=2):
        """Create a connection to the console overseer, setting `self.ws_protocol`."""
        for i in range(0, retry_num):
            try:
                transport, protocol = self.loop.run_until_complete(self.loop.create_connection(WebclientCommunicationProtocol, host=address, port=port))
                self.ws_protocol = protocol
                self.ws_protocol.cons = self
                self.ws_protocol.send_message(json.dumps({
                    'username': self.username,
                    'connection_code': self.connection_code
                }))
                break
            except ConnectionRefusedError:
                print(f"Connection refused; retrying in {delay} seconds...", file=sys.stderr)
                time.sleep(delay)
                delay *= 2
                continue
    
    def shut_down(self):
        self.protocol.send_message(json.dumps({
            'type': 'quit',
            'data': 'Disconnected from gameserver.'
        }))
    
    def init_connection(self, data_str):
        if self.auto_load_player:
            if self.current_player_name:
                self._load_player_from_file(data_str, self.current_player_name)
            else:
                self.write_output("Please name your character, or enter a console command:")
    
    def handle_command(self, input_str):
        return super().handle_command(input_str, additional_cmds_map={}, call_on_quit=self.shut_down)
    
    def upload_file(self, file_contents, filename):
        """Upload a file to the filesystem. This includes loading files that were opened for editing."""
        if self.wizard_privilages():
            try:
                f = open(filename, "w")
                f.write(file_contents)
                f.close()
                self.write_output("Sucessfully uploaded file.")
            except Exception as e:
                self.write_output("An error occured when upload the file. The error: "+e)
        else:
            self.write_output("Wizard privilages are required to upload and download files.")
    
    def download_file(self, filename, for_edit=False):
        """Download a file to the user. This includes opening files for editing."""
        if self.wizard_privilages():
            try:
                f = open(filename, "r")
                file_contents = f.read()
                f.close()
            except Exception as e:
                self.write_output("An error occured when trying to download the file. The error: "+e)
            else:
                self.ws_protocol.send_message(json.dumps({
                    'type': 'file',
                    'data': file_contents,
                    'filename': filename,
                    'for_edit': for_edit
                }))
        else:
            self.write_output("Wizard privilages are required to upload and download files.")

    def write_output(self, *output_strs, sep="", message_type="response"):
        """Write the given output to the webclient."""
        message_str = sep.join(output_strs)
        message_str = self.choose_measurements(message_str)
        message_str = self.sanitizeHTML(message_str)
        message_dict = {
            'type': message_type,
            'data': message_str,
            'version': self.WebclientProtocolVersion
        }
        message_json = json.dumps(message_dict)
        self.ws_protocol.send_message(message_json)

    async def read_input(self):
        """This is a blank implementation of the function, as it is not necessary in this version of the console."""

if __name__ == "__main__":
    connection_code = sys.argv[1]
    username = sys.argv[2]
    gameserver_host = '127.0.0.1'
    gameserver_port = 9123
    ws_host = "127.0.0.1"
    ws_port = 9125
    console = WebclientConsole(username, gameserver_host, gameserver_port, ws_host, ws_port, connection_code)
    console.startup_console()