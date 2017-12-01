import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        print("received message '%s'" % message)
        await websocket.send(message)
        print("Sent message '%s'" % message)
        

asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, '127.0.0.1', 9124))
asyncio.get_event_loop().run_forever()