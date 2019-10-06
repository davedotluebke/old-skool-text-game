import asyncio
import websockets
import os.path
import random
import time
try:
    import sjcl
    encryption_installed = True
except ModuleNotFoundError:
    print("sjcl not installed. Running wihtout...")
    encryption_installed = False
import json
import base64
import functools

from thing import Thing
from console import Console
import gametools
from debug import dbg

# From the websockets.serve() documentation:
# Since there's no useful way to propagate exceptions triggered in handlers,
# they're sent to the 'websockets.server' logger instead. Debugging is much
# easier if you configure logging to print them:
import logging
logger = logging.getLogger('websockets.server')
logger.setLevel(logging.ERROR)
logger.addHandler(logging.StreamHandler())   

conn_to_client = {}
encryption_enabled = True
if encryption_installed:
    crypto_obj = sjcl.SJCL()

async def ws_handler(websocket, path):
    try: 
        async for encrypted_message in websocket:
            try:
                cons = conn_to_client[websocket]
                message = json.loads(encrypted_message)
                if encryption_enabled:
                    message['ct'] = message['ct'].encode('utf-8')
                    message['iv'] = message['iv'].encode('utf-8')
                    message['salt'] = message['salt'].encode('utf-8')
                    decrypted_message = crypto_obj.decrypt(message, cons.encode_str)
                    text_message = str(decrypted_message, 'utf-8')
                    message_dict = json.loads(text_message)
                else:
                    message_dict = message
                data = message_dict['data']
                if message_dict['type'] == 'command':
                    cons.raw_input += data
                elif message_dict['type'] == 'file':
                    data = base64.b64decode(data) 
                    cons.file_input = data 
                    if 'filename' in message_dict and message_dict['filename'] != '':
                        cons.filename_input = message_dict['filename']
                    else:
                        cons.filename_input = 'default_filename.py'
                    dbg.debug('File added to file input!', 2)
            except KeyError:
                cons = Console(websocket, Thing.game, encrypted_message)
                conn_to_client[websocket] = cons
                try:
                    Thing.game.login_player(cons)
                except gametools.PlayerLoadError:
                    Thing.game.create_new_player(name, cons)
            except IndexError:
                dbg.debug('IndexError in connections_websock!')
    except websockets.exceptions.ConnectionClosed:
        websocket.close()

async def ws_send(cons):
    output = json.dumps({"type": "response", "data": cons.raw_output})
    if encryption_enabled:
        output = bytes(output, 'utf-8')
        output = crypto_obj.encrypt(output, cons.encode_str)
        for i in output:
            if isinstance(output[i], bytes):
                output[i] = output[i].decode('utf-8')
        output = json.dumps(output)
    cons.raw_output = ''
    await cons.connection.send(output)

async def file_send(cons):
    raw_file = cons.file_output
    b64_file = str(base64.b64encode(raw_file), "utf-8")
    json_output = json.dumps({"type": "file", "data": b64_file})
    if encryption_enabled:
        json_bytes = bytes(json_output, "utf-8")
        output = crypto_obj.encrypt(json_bytes, cons.encode_str)
        for i in output:
            if isinstance(output[i], bytes):
                output[i] = output[i].decode('utf-8')
        final_output = json.dumps(output)
    else:
        final_output = json_output
    cons.file_output = bytes()
    await cons.connection.send(final_output)
