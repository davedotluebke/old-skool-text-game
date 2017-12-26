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
                name = 'randomplayer' + random.randint(10, 99)
            try:
                Thing.game.load_player(os.path.join(gametools.PLAYER_DIR, name), cons)
            except gametools.PlayerLoadError:
                Thing.game.create_new_player(name, cons)
            #XXX temp hack ends
    

async def ws_send(cons):
    await cons.connection.send(cons.raw_output)
    






'''
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

    asyncio.get_event_loop().call_later(ws_handler(functools.partial(ws_handler, websocket, path)))


# The callback that consumes messages from the client:
async def ws_consumer_handler(websocket, user_cons):
    async for message in websocket:
        print("received message '%s' from client %s" % (message, user_cons))
        user_cons.raw_input += (message + '\n')

async def ws_producer_handler(websocket, user_cons): 
    message = await producer(user_cons)
    if message != '':
        await websocket.send(message)

async def producer(user_cons):
    output = user_cons.raw_output
    user_cons.raw_output = ''
    return output
'''
