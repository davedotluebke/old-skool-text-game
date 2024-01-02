# this module is intended for connecting to the game when a web browser or internet is not available
# it does not support encryption and assumes a secure connection

import asyncio
import websockets

async def ws_handler(websocket, path):
    try: 
        async for message in websocket:
            print(message)
    except websockets.exceptions.ConnectionClosed:
        websocket.close()

async def ws_send(text):
    await connection.send(text)

ip_address = input('IP Address: ')
port = input('Port: ')

connection = asyncio.get_event_loop().run_until_complete(websockets.connect("ws://" + ip_address + ":" + port))
