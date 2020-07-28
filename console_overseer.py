import asyncio
import subprocess
import websockets
import sys
import random
import json
from secrets import token_hex

# From the websockets.serve() documentation:
# Since there's no useful way to propagate exceptions triggered in handlers,
# they're sent to the 'websockets.server' logger instead. Debugging is much
# easier if you configure logging to print them:
import logging
logger = logging.getLogger('websockets.server')
logger.setLevel(logging.ERROR)
logger.addHandler(logging.StreamHandler())

PASSWORDS_FILE = '/home/%s/passwords.sec' % subprocess.run(['whoami'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip() # do this so outside of git realm
# START_CONSOLE_CMD = 'sudo -bu %s python3 /game/console.py --connection-code "%s" "%s"'
START_CONSOLE_CMD = ['sudo', '-bu', '%s', 'python3', 'console.py', '%s', '%s']
try:
    DEFAULT_CONSOLE_USER = sys.argv[1]
except IndexError:
    DEFAULT_CONSOLE_USER = 'nwconsole'

SERVER_IP = '127.0.0.1' # XXX set this dynamically
WS_SERVER_PORT = 9124 # XXX also set this dynamically
RS_SERVER_PORT = 9125 # XXX also set this dynamically

ws_usernames = {}
ws_connection_state = {}
ws_connection_modes = {}

rs_usernames = {}

connection_codes = []

loop = None

class GameWebsocketServer:
    """A websocket server for the game."""
    async def ws_handler(self, websocket, path):
        try:
            async for message_str in websocket:
                try:
                    # find the username of an existing connection
                    username, connection_code = ws_usernames[websocket]
                    connection_state = ws_connection_state[websocket]
                except KeyError:
                    # new connection, create new username entry
                    username = None
                    connection_code = token_hex(32)
                    while connection_code in connection_codes:
                        connection_code = token_hex(32) # make sure that connection codes are unique
                    connection_codes.append(connection_code)
                    ws_usernames[websocket] = [username, connection_code]
                    ws_connection_state[websocket] = 'AWAITING_LOGIN'
                    ws_connection_modes[websocket] = 'standard'
                    connection_state = 'AWAITING_LOGIN'
                
                if connection_state == 'CONSOLE_CONNECTED':
                    send_to_console(username, connection_code, message_str)
                else:
                    if message_str == "Connected!":
                        self.jsonify_and_send(username, connection_code, 'Welcome! Please enter your username:')
                        continue
                    message_dict = json.loads(message_str)
                    try:
                        message_type = str(message_dict['type'])
                        message_data = str(message_dict['data']).strip()
                    except KeyError:
                        print("Invalid JSON dictionary!")
                        continue

                    legacy_mode = ws_connection_modes[websocket] == 'legacy'

                    # Note: message types of 'command' are included for legacy support.

                    if connection_state == 'AWAITING_LOGIN' and message_type in ['login', 'command']:
                        if not 'version' in message_dict.keys():
                            legacy_mode = True
                            ws_connection_modes[websocket] = 'legacy'
                        for i in list(ws_usernames):
                            if ws_usernames[i][0] == message_data:
                                self.jsonify_and_send(username, connection_code, f'A connection for {message_data} is already open. Opening another connection to {message_data} will close the first one. Are you sure you would like to do this? [Y/n]', message_type='confirmation')
                                connection_state = 'AWAITING_RECONNECT_CONFIRM'
                                break
                        else:
                            f = open(PASSWORDS_FILE, 'r')
                            user_exits = message_data in list(json.loads(f.read()))
                            f.close()
                            ws_usernames[websocket][0] = message_data
                            username = message_data
                            if user_exits:
                                self.jsonify_and_send(username, connection_code, f"Welcome back, {message_data}! Now please enter your {'--#password' if legacy_mode else 'password'}:", message_type='password_request')
                                connection_state = 'AWAITING_PASSWORD'
                            else:
                                self.jsonify_and_send(username, connection_code, f'No user named {message_data} found. Would you like to create a new user?', message_type='confirmation')
                                connection_state = 'AWAITING_CREATE_CONFIRM'
                    elif connection_state == 'AWAITING_CREATE_CONFIRM' and (message_type == 'input' or legacy_mode):
                        if message_data.lower() in ['yes', 'y', 'confirm']:
                            self.jsonify_and_send(username, connection_code, f"Creating a new user named {username}. Please create a {'--#password' if legacy_mode else 'password'}:", message_type='password_request')
                            connection_state = 'AWAITING_NEW_PASSWORD'
                        elif message_data.lower() in ['no', 'n', 'cancel']:
                            self.jsonify_and_send(username, connection_code, 'Okay, please enter your username:')
                            connection_state = 'AWAITING_LOGIN'
                        else:
                            self.jsonify_and_send(username, connection_code, "Please answer yes or no:")
                    elif connection_state == 'AWAITING_NEW_PASSWORD' and (message_type == 'password' or legacy_mode):
                        # TODO: Hash the password again here
                        try:
                            f = open(PASSWORDS_FILE, 'r')
                            old_json = f.read()
                            passwords_dict = json.loads(old_json)
                            f.close()
                            success = True
                        except Exception as e:
                            self.jsonify_and_send(username, connection_code, f'A error occured! The error: {e}')
                            success = False
                        passwords_dict[username] = message_data
                        if success:
                            try:
                                f = open(PASSWORDS_FILE, 'w')
                                f.write(json.dumps(passwords_dict))
                                f.close()
                                self.jsonify_and_send(username, connection_code, f'Your new user has been created.')
                                username_to_run_in = DEFAULT_CONSOLE_USER
                                list_of_wizards = subprocess.run(['getent', 'group', 'wizards'], stdout=subprocess.PIPE).stdout.decode('utf-8').split(":")[-1].strip().split(",")
                                if username in list_of_wizards:
                                    username_to_run_in = username
                                st_cmd = START_CONSOLE_CMD
                                st_cmd[2] = username_to_run_in
                                st_cmd[5] = connection_code
                                st_cmd[6] = username
                                subprocess.run(st_cmd)
                                connection_state = 'AWAITING_CONSOLE_CONNECTION'
                            except Exception as e:
                                self.jsonify_and_send(username, connection_code, f'A error occured! The error: {e}')
                                f.write(old_json)
                                f.close()
                    elif connection_state == 'CHANGING_PASSWORD' and (message_type == 'password' or legacy_mode):
                        # TODO: Hash the password again here
                        try:
                            f = open(PASSWORDS_FILE, 'r')
                            old_json = f.read()
                            passwords_dict = json.loads(old_json)
                            f.close()
                            success = True
                        except Exception as e:
                            self.jsonify_and_send(username, connection_code, f'A error occured! The error: {e}')
                            success = False
                        passwords_dict[username] = message_data
                        if success:
                            try:
                                f = open(PASSWORDS_FILE, 'w')
                                f.write(json.dumps(passwords_dict))
                                f.close()
                                self.jsonify_and_send(username, connection_code, 'Your password has been updated.')
                                connection_state = 'CONSOLE_CONNECTED'
                            except Exception as e:
                                self.jsonify_and_send(username, connection_code, f'A error occured! The error: {e}')
                                f.write(old_json)
                                f.close()
                    elif connection_state == 'AWAITING_RECONNECT_CONFIRM' and (message_type == 'input' or legacy_mode):
                        if message_data.lower() in ['yes', 'y', 'confirm']:
                            self.jsonify_and_send(username, connection_code, f"Taking over input upon password. Please enter your {'--#password' if legacy_mode else 'password'}:", message_type='password_request')
                            connection_state = 'AWAITING_PASSWORD'
                        elif message_data.lower() in ['no', 'n', 'cancel']:
                            self.jsonify_and_send(username, connection_code, 'Okay, please enter your username:')
                            connection_state = 'AWAITING_LOGIN'
                        else:
                            self.jsonify_and_send(username, connection_code, "Please answer yes or no:")
                    elif connection_state == 'AWAITING_PASSWORD' and (message_type == 'password' or legacy_mode):
                        # TODO: Hash the password again here
                        try:
                            f = open(PASSWORDS_FILE, 'r')
                            password_correct = message_data == json.loads(f.read())[username]
                            f.close()
                        except Exception as e:
                            self.jsonify_and_send(username, connection_code, f'An error occured! The error: {e}')
                            password_correct = False
                        if password_correct:
                            username_to_run_in = DEFAULT_CONSOLE_USER
                            list_of_wizards = subprocess.run(['getent', 'group', 'wizards'], stdout=subprocess.PIPE).stdout.decode('utf-8').split(":")[-1].strip().split(",")
                            if username in list_of_wizards:
                                username_to_run_in = username
                            st_cmd = START_CONSOLE_CMD
                            st_cmd[2] = username_to_run_in
                            st_cmd[5] = connection_code
                            st_cmd[6] = username
                            subprocess.run(st_cmd)
                            connection_state = 'AWAITING_CONSOLE_CONNECTION'
                        else:
                            self.jsonify_and_send(username, connection_code, 'Your username or password was incorrect. Please enter your username:')
                            connection_state = 'AWAITING_LOGIN'
                    elif connection_state == 'AWAITING_CONSOLE_CONNECTION':
                        self.jsonify_and_send(username, connection_code, 'You are being connected to the console. Please wait.')
                    else:
                        self.jsonify_and_send(username, connection_code, f'The connection state was {connection_state} but the message type was {message_type}, matching no known sequence! Please try again.')
                    ws_connection_state[websocket] = connection_state

        except websockets.exceptions.ConnectionClosed:
            websocket.close()

    async def ws_send(self, username, connection_code, message_json):
        for i in list(ws_usernames): # XXX is there a better method here?
            if ws_usernames[i][0] == username and ws_usernames[i][1] == connection_code:
                await i.send(message_json)
                break
        else:
            print(f"No matching username and connection code. Username: {username}. Connection code: {connection_code}")

    def jsonify_and_send(self, username, connection_code, message_data, message_type="response"):
        if ws_connection_modes[[i for i in list(ws_usernames) if ws_usernames[i][1] == connection_code][0]] == "legacy" and message_type not in ["file", "response"]:
            message_type = "response"
            print("legacy mode detected")
        message_dict = {
            "type": message_type,
            "data": message_data
        }
        message_json = json.dumps(message_dict)
        asyncio.ensure_future(self.ws_send(username, connection_code, message_json))

game_ws_server = GameWebsocketServer()

class ConsoleConnectionProtocol(asyncio.Protocol):
    """A protocol for communicating with consoles."""
    def connection_made(self, transport):
        self.transport = transport
        self.mode = "CONNECTING"
    
    def connection_lost(self, exc):
        return super().connection_lost(exc)
    
    def data_received(self, data):
        global ws_connection_modes
        global ws_usernames
        data_str = data.decode('utf-8')
        data_json_list = data_str.split('\u0004')
        for data_json in data_json_list:
            if not data_json:
                continue
            data_json = data_json.strip()
            data_dict = json.loads(data_json)
            if self.mode == "CONNECTED":
                try:
                    data_type = data_dict['type']
                    if data_type == "quit":
                        self.transport.close()
                        if ws_connection_modes[[i for i in list(ws_usernames) if ws_usernames[i][1] == self.connection_code][0]] == "legacy":
                            print("legacy mode, sending --#quit")
                            asyncio.ensure_future(game_ws_server.jsonify_and_send(self.username, self.connection_code, "--#quit"))
                            continue
                    elif data_type == "password_request":
                        ws_connection_state[[i for i in list(ws_usernames) if ws_usernames[i][1] == self.connection_code][0]] = "CHANGING_PASSWORD"
                        if ws_connection_modes[[i for i in list(ws_usernames) if ws_usernames[i][1] == self.connection_code][0]] == "legacy":
                            asyncio.ensure_future(game_ws_server.jsonify_and_send(self.username, self.connection_code, "Please enter a new --#password"))
                            continue
                except KeyError:
                    pass
                asyncio.ensure_future(game_ws_server.ws_send(self.username, self.connection_code, data_json))
            elif self.mode == "CONNECTING":
                try:
                    self.username = data_dict['username']
                    self.connection_code = data_dict['connection_code']
                    rs_usernames[self.username] = self
                    self.mode = "CONNECTED"
                    self.send_message(json.dumps({
                        "type": "connection_init",
                        "data": "The connection was successfully established."
                    }))
                    ws_connection_state[[i for i in list(ws_usernames) if ws_usernames[i][1] == self.connection_code][0]] = "CONSOLE_CONNECTED"
                except KeyError:
                    pass
            else:
                print("ERROR!")

    def send_message(self, msg_json):
        self.transport.write(msg_json.encode('utf-8')+'\u0004'.encode('utf-8'))


def send_to_console(username, connection_code, message_json):
    try:
        ccp = rs_usernames[username]
    except KeyError:
        print(f'No console with the name {username} found.')
        return
    if ccp.connection_code == connection_code:
        ccp.send_message(message_json)
    else:
        print("Please provide the correct connection code.")

def start_servers():
    """Start and connect the two servers."""
    global loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(websockets.serve(game_ws_server.ws_handler, SERVER_IP, WS_SERVER_PORT))
    loop.run_until_complete(loop.create_server(ConsoleConnectionProtocol, '127.0.0.1', RS_SERVER_PORT))
    loop.run_forever()

if __name__ == "__main__":
    start_servers()