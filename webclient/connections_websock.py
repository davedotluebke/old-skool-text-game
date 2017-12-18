import asyncio
import websockets

# From the websockets.serve() documentation:
# Since there's no useful way to propagate exceptions triggered in handlers,
# they're sent to the 'websockets.server' logger instead. Debugging is much
# easier if you configure logging to print them:
import logging
logger = logging.getLogger('websockets.server')
logger.setLevel(logging.ERROR)
logger.addHandler(logging.StreamHandler())   

# The callback that does everything in the webserver:
async def handler_callback(websocket, path):
    async for message in websocket:
        print("received message '%s'" % message)
        message = "I, the server, reply: " + message
        await websocket.send(message)
        websocket.
        print("Sent message '%s'" % message)



asyncio.get_event_loop().run_until_complete(
    websockets.serve(handler_callback, '127.0.0.1', 9124))
asyncio.get_event_loop().run_forever()

