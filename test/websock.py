import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        print("received message '%s'" % message)
        message = "my reply: " + message
        await websocket.send(message)
        print("Sent message '%s'" % message)

# From the websockets.serve() documentation:
# Since there's no useful way to propagate exceptions triggered in handlers,
# they're sent to the 'websockets.server' logger instead. Debugging is much
# easier if you configure logging to print them:
import logging
logger = logging.getLogger('websockets.server')
logger.setLevel(logging.ERROR)
logger.addHandler(logging.StreamHandler())   

asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, '127.0.0.1', 9124))
asyncio.get_event_loop().run_forever()

