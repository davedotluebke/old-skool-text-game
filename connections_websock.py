import asyncio
import websockets
import os.path
import random
import functools

from thing import Thing
from console import Console
import gametools

# From the websockets.serve() documentation:
# Since there's no useful way to propagate exceptions triggered in handlers,
# they're sent to the 'websockets.server' logger instead. Debugging is much
# easier if you configure logging to print them:
import logging
logger = logging.getLogger('websockets.server')
logger.setLevel(logging.ERROR)
logger.addHandler(logging.StreamHandler())   

conn_to_client = {}

async def ws_handler(websocket, path):
    async for message in websocket:
        try:
            conn_to_client[websocket].raw_input += message
        except KeyError:
            cons = Console(websocket, Thing.game)
            conn_to_client[websocket] = cons
            # XXX temporary hack to postpone hooking up login code to Console
            if len(conn_to_client) == 1:
                name = 'cedric'
            elif len(conn_to_client) == 2:
                name = 'alex'
            else:
                name = 'randomplayer' + str(random.randint(10, 99))
            try:
                Thing.game.load_player(os.path.join(gametools.PLAYER_DIR, name), cons)
            except gametools.PlayerLoadError:
                Thing.game.create_new_player(name, cons)
            #XXX temp hack ends
    

async def ws_send(cons):
    output = cons.raw_output
    cons.raw_output = ''
    await cons.connection.send(output)
