import asyncio
import websockets

async def echo(websocket, path):
    try:
        while True:
            message = await websocket.recv()
            await websocket.send(message)
            print('sent message ' + message)
    except websockets.exceptions.ConnectionClosed:
        print('The connection was closed.')

asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 9124))
asyncio.get_event_loop().run_forever()