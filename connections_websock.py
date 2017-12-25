import asyncio
import websockets
import os.path
import random

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

clients = dict()  # dictionary mapping client consoles to their websockets

# The callback that does everything in the webserver:
async def ws_handler(websocket, path):
    # figure out which client this handler corresponds to
    global clients  
    try: 
        client_cons = clients[websocket]
    except KeyError:
        print("websocket not associated with a client, making new client!")
        client_cons = Console(websocket, Thing.game)
        clients[websocket] = client_cons
        # XXX temporary hack to postpone hooking up login code to Console
        if len(clients) == 1:
            name = 'cedric'
        elif len(clients) == 2:
            name = 'alex'
        else:
            name = 'randomplayer' + random.randint(10, 99)
        try:
            Thing.game.load_player(os.path.join(gametools.PLAYER_DIR, name), client_cons)
        except gametools.PlayerLoadError:
           Thing.game.create_new_player(name, client_cons)

    consumer_task = asyncio.ensure_future(ws_consumer_handler(websocket, client_cons))
    producer_task = asyncio.ensure_future(ws_producer_handler(websocket, client_cons))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    # XXX why cancel pending tasks? 
    for task in pending:
        task.cancel()


# The callback that consumes messages from the client:
async def ws_consumer_handler(websocket, user_cons):
    async for message in websocket:
        print("received message '%s' from client %s" % (message, user_cons))
        user_cons.raw_input += (message + '\n')

async def ws_producer_handler(websocket, user_cons): 
    while True: 
        message = await producer(user_cons)
        await websocket.send(message)

async def producer(user_cons):
    output = user_cons.raw_output
    user_cons.raw_output = ''
    return output
