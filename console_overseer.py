import asyncio
import subprocess
import websockets
import random
import json

# From the websockets.serve() documentation:
# Since there's no useful way to propagate exceptions triggered in handlers,
# they're sent to the 'websockets.server' logger instead. Debugging is much
# easier if you configure logging to print them:
import logging
logger = logging.getLogger('websockets.server')
logger.setLevel(logging.ERROR)
logger.addHandler(logging.StreamHandler())

PASSWORDS_FILE = 'passwords.sec'

ws_usernames = {}
ws_connection_state = {}
ws_connection_modes = {}
connection_codes = []

async def ws_handler(websocket, path):
    try:
        async for message_str in websocket:
            try:
                # find the username of an existing connection
                username, connection_code = ws_usernames[websocket]
                connection_state = ws_connection_state[websocket]
            except KeyError:
                # new connection, create new username entry
                username = None
                connection_code = random.random()
                while connection_code in connection_codes:
                    connection_code = random.random() # make sure that connection codes are unique
                connection_codes.append(connection_code)
                ws_usernames[websocket] = [username, connection_code]
                ws_connection_states[websocket] = 'AWAITING_LOGIN'
                ws_connection_modes[websocket] = 'standard'
                connection_state = 'AWAITING_LOGIN'
            
            if connection_state == 'CONSOLE_CONNECTED':
                send_to_console(username, connection_code, message_str)
            else:
                message_dict = json.loads(message_str)
                message_type = str(message_dict['type'])
                message_data = str(message_dict['data'])

                legacy_mode = ws_connection_modes[websocket] == 'legacy'

                # Note: message types of 'command' are included for legacy support.

                if connection_state == 'AWAITING_LOGIN' and message_type in ['login', 'command']:
                    if message_type == 'command':
                        legacy_mode = True
                        ws_connection_modes[websocket] == 'legacy'
                    for i in list(ws_usernames):
                        if ws_usernames[i][0] == message_data:
                            jsonify_and_send(username, connection_code, f'A connection for {message_data} is already open. Opening another connection to {message_data} will close the first one. Are you sure you would like to do this? [Y/n]', type='confirmation')
                            connection_state = 'AWAITING_RECONNECT_CONFIRM'
                            break
                    else:
                        ws_usernames[websocket][0] = message_data
                        jsonify_and_send(username, connection_code, f'Welcome back, {message_data}! Now please enter your {'--#password' if legacy_mode else 'password'}:', type='password_request')
                elif connection_state == 'AWAITING_RECONNECT_CONFIRM' and (message_type == 'input' or legacy_mode):
                    if message_data.lower() in ['yes', 'y', 'confirm']:
                        jsonify_and_send(username, connection_code, f'Taking over input upon password. Please enter your {'--#password' if legacy_mode else 'password'}:', type='password_request')
                        connection_state = 'AWAITING_PASSWORD'
                    elif message_data.lower() in ['no', 'n', 'cancel']:
                        jsonify_and_send(username, connection_code, 'Okay, please enter your username:')
                        connection_state = 'AWAITING_LOGIN'
                    else:
                        jsonify_and_send(username, connection_code, "Please answer yes or no:")
                elif connection_state == 'AWAITING_PASSWORD' and (message_type == 'password' or legacy_mode):
                    # TODO: Hash the password again here
                    try:
                        f = open(PASSWORDS_FILE, 'r')
                        json.loads(f.read())
                        f.close()
                        password_correct = message_data == json.loads(f.read())[username]
                    except Exception as e:
                        jsonify_and_send(username, connection_code, f'An error occured! The error: {e}')
                        password_correct = False
                    if password_correct:
                        connection_state = 'AWAITING_CONSOLE_CONNECTION'
                    else:
                        jsonify_and_send(username, connection_code, 'Your username or password was incorrect. Please enter your username:')
                        connection_state = 'AWAITING_LOGIN'
                elif connection_state == 'AWAITING_CONSOLE_CONNECTION':
                    jsonify_and_send(username, connection_code, 'You are being connected to the console. Please wait.')
                else:
                    jsonify_and_send(username, connection_code, f'The connection sate was {connection_state} but the message type was {message_type}, matching no known sequence! Please try again.')
                ws_connection_states[websocket] = connection_state

    except websockets.exceptions.ConnectionClosed:
        websocket.close()


start_command = 'sudo -bu %s python3 /game/console.py'
subprocess.run(['getent', 'group', 'wizards'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8').split(":")[-1].strip().split(",")

