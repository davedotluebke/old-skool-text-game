import asyncio
import websockets
import os.path
import random
import time
import sjcl
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
crypto_obj = sjcl.SJCL()

async def ws_handler(websocket, path):
    try: 
        async for message in websocket:
            try:
                cons = conn_to_client[websocket]
                message = json.loads(message)
                message['ct'] = message['ct'].encode('utf-8')
                message['iv'] = message['iv'].encode('utf-8')
                message['salt'] = message['salt'].encode('utf-8')
                message = crypto_obj.decrypt(message, cons.encode_str)
                message = str(message, 'utf-8')
                message = json.loads(message)
                data = message['data']
                if message['type'] == 'command':
                    cons.raw_input += message['data']
                elif message['type'] == 'file':
                    data = base64.b64decode(data) 
                    cons.file_input = data 
                    dbg.debug('File added to file input!', 2)
            except KeyError:
                cons = Console(websocket, Thing.game, message)
                conn_to_client[websocket] = cons
                try:
                    Thing.game.login_player(cons)
                except gametools.PlayerLoadError:
                    Thing.game.create_new_player(name, cons)
            except IndexError:
                pass
    except websockets.exceptions.ConnectionClosed:
        websocket.close()

async def ws_send(cons):
    output = json.dumps({"type": "response", "data": cons.raw_output})
    output = bytes(output, 'utf-8')
    output = crypto_obj.encrypt(output, cons.encode_str)
    for i in output:
        if isinstance(output[i], bytes):
            output[i] = output[i].decode('utf-8')
    output = json.dumps(output)
    cons.raw_output = ''
    await cons.connection.send(output)

async def file_send(cons):
    output = cons.file_output
    output = crypto_obj.encrypt(output, cons.encode_str)
    cons.file_output = bytes()
    await cons.connection.send(output)
