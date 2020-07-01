import asyncio
import functools
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
        return super().connection_lost(exc)
    
    def data_received(self, data):
        self.cons.receive_from_gameserver(data.decode('utf-8'))
    
    def send_message(self, message):
        self.transport.write(message.encode('utf-8'))

class BaseConsole:
    """A base class for all game consoles, containing the basic code to
    communicate with the game server and to run shell commands. Subclasses
    provide more functionality."""
    saved_attributes = ["current_player_name"] # attributes that the console should save in its config file
    def __init__(self, username, gameserver_host, gameserver_port):
        self.username = username
        self.loop = asyncio.get_event_loop()
        # items related to connection to gameserver
        self.connect_to_gameserver(gameserver_host, gameserver_port)
        self.protocol = None
        self.gameserver_input = []
        self.gameserver_output = []
        # items related to bash shell integration
        self.loop.run_until_complete(self._setup_bash_console())
        self.bash_output = b''
        self.bash_input = ''
        # user input information (subclasses provide more functionality)
        self.current_string = ''
        # player save/load information
        self.current_player_name = None
        # start the console
        self.startup_console()
    
    #
    # Functions related to console startup and shutdown
    #

    def startup_console(self):
        """Start the asyncio event loop, first loading saved attributes
        (such as player name, and eventually aliases etc). When the loop
        exits, save those attributes again."""
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

        self.loop.call_later(1, self.read_input)
        self.loop.run_forever()

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
            self.write_output("Error unpacking JSON message from server!")
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
                error_code = message_dict['error-code']
                self.write_output("An error occurred in the request.")
                self.write_output(f"Error code: {error_code} ({gametools.console_error_codes[error_code]["name"]})")
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
                f = open(f'saved_players/{self.current_player_name}.OADplayer', 'w')
                f.write(player_json)
                f.close()
            except Exception as e:
                self.write_output("An error occurred while saving the player. Printing below: \n"+e)
                return
            
        else:
            self.write_output(f"The message type is not supported. Message type: {message_type}")

    def send_to_gameserver(self, type, message=None, player_json=None):
        message_dict = {
            "type": type
        }
        if message:
            message_dict["message"] = message
        if player_json:
            message_dict["player_json"] = player_json
        try:
            message_json = json.dumps(message_dict)
        except Exception as e:
            self.write_output("An error occurred preparing the message for the gameserver. Error message: "+e)
            return
        self.protocol.send_message(message_json)
    
    #
    # Functions for running commands in the bash subprocess
    #
    
    async def _setup_bash_console(self):
        """Create the bash process, and begin reading and writing from it."""
        self.bash_process = asyncio.create_subprocess_exec('bash', stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        await asyncio.gather(self._read_bash_stderr(self.bash_process.stderr), self._read_bash_stdeout(self.bash_process.stdout), self._write_bash_stdin(self.bash_process.stdin))
    
    async def _read_bash_stderr(self, stderr):
        """Read the stderr of the bash process."""
        while True:
            buf = await stderr.read()
            if not buf:
                break
            self.bash_output += buf

    async def _read_bash_stdeout(self, stdout):
        """Read the stdout of the bash process."""
        while True:
            buf = await stdout.read()
            if not buf:
                break
            self.bash_output += buf
    
    async def _write_bash_stdin(stdin):
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
            f = open(f"saved_players/{player_name}")
            player_json = f.read()
            f.close()
            self.current_player_name = player_name
            return False
        except FileNotFoundError:
            self.write_output(f"No player named {player_name} found. To create a new player, type 'create {player_name}")
        except PermissionError:
            self.write_output(f"The player {player_name} is not yours. Please try again.")
        except Exception as e:
            self.write_output(e)
        return True
        
    def handle_command(self, input_str):
        """Decide what to do with a user command: 
        - pass to gameserver,
        - pass to shell, or
        - save and load a player."""
        input_words = input_str.split(" ")
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
            if _load_player_from_file(input_words, player_name):
                return

        elif input_words[0] == "create":

    def write_output(self, *output_strs):
        """Write the given output. Must be subclassed for additional functionality."""
        raise NotImplementedError("write_output must be subclassed")

    def read_input(self):
        """Read the current input. Must be subclassed for additional functionality."""
        raise NotImplementedError("read_input must be subclassed")

