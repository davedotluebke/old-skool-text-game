import asyncio
import websockets
import os.path
import random
import time
import sjcl
import json
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
                start_time = time.time()
                #print('------')
                cons = conn_to_client[websocket]
                #print(time.time() - start_time)
                message = json.loads(message)
                #print(time.time() - start_time)
                message['ct'] = message['ct'].encode('utf-8')
                message['iv'] = message['iv'].encode('utf-8')
                message['salt'] = message['salt'].encode('utf-8')
                #print(time.time() - start_time)
                message = crypto_obj.decrypt(message, cons.encode_str)
                #print(time.time() - start_time)
                cons.raw_input += str(message, 'utf-8')
                #print(time.time() - start_time)
            except KeyError:
                cons = Console(websocket, Thing.game, message)
                conn_to_client[websocket] = cons
                try:
                    Thing.game.login_player(cons)
                except gametools.PlayerLoadError:
                    Thing.game.create_new_player(name, cons)
            except TypeError:
                conn_to_client[websocket].file_input = message
                dbg.debug('File added to file input!', 2)
                print('File added to file input!')
    except websockets.exceptions.ConnectionClosed:
        websocket.close()

async def ws_send(cons):
    start_time = time.time()
    #print('------')
    output = bytes(cons.raw_output, 'utf-8')
    #print(time.time() - start_time)
    output = crypto_obj.encrypt(output, cons.encode_str)
    #print(time.time() - start_time)
    for i in output:
        if isinstance(output[i], bytes):
            output[i] = output[i].decode('utf-8')
    #print(time.time() - start_time)
    output = json.dumps(output)
    #print(time.time() - start_time)
    cons.raw_output = ''
    await cons.connection.send(output)

async def file_send(cons):
    output = cons.file_output
    output = crypto_obj.encrypt(output, cons.encode_str)
    cons.file_output = bytes()
    await cons.connection.send(output)
