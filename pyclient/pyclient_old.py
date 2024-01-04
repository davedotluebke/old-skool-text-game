# this module is intended for connecting to the game when a web browser or internet is not available
# it does not support encryption and assumes a secure connection

import asyncio
import websockets

ip_address = input('IP Address: ')
port = input('Port: ')

raw_input = ""

def take_input():
    global raw_input
    raw_input += input('> ') + "\n"
    asyncio.get_event_loop().call_later(0.1, take_input)

async def main():
    async with websockets.connect("ws://" + ip_address + ":" + port) as ws:
        while True:
            if raw_input:
                ws.send(raw_input.partition("\n")[0])
            msg = await ws.recv()
            if msg:
                print(msg)

asyncio.get_event_loop().call_later(0.1, take_input)
connection = asyncio.get_event_loop().run_until_complete(main())
