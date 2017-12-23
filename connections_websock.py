import asyncio
import websockets
from thing import Thing
from console import Console

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
async def handler_callback(websocket, path):
    # figure out which client this handler corresponds to
    global clients  
    try: 
        client_cons = clients[websocket]
    except KeyError:
        print("websocket not associated with a client, making new client!")
        client_cons = Console(websocket, Thing.game)
        clients[websocket] = client_cons

    async for message in websocket:
        print("received message '%s' from client %s" % (message, client_cons))
        message = "I, the server, reply: " + message
        await websocket.send(message)
        
        print("Sent message '%s'" % message)



asyncio.get_event_loop().run_until_complete(
    websockets.serve(handler_callback, '127.0.0.1', 9124))
asyncio.get_event_loop().run_forever()

