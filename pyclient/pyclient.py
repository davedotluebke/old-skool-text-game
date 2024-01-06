import asyncio
import json
from websockets import connect

import non_blocking_input

raw_input = "Initiating connection"

def add_raw_input(inp):
    global raw_input
    raw_input += inp + "\n"

async def send_input():
    async with connect("ws://localhost:9124") as websocket:
        asyncio.ensure_future(await_output(websocket))
        global raw_input
        while True:
            if raw_input:
                json_s = {
                    "type": "command",
                    "data": raw_input.partition("\n")[0]
                }
                raw_input = raw_input.partition("\n")[2]
                await websocket.send(json.dumps(json_s))
            await asyncio.sleep(0.1)

async def await_output(websocket):
    while True:
        message = await websocket.recv()
        print(json.loads(message)['data'])

kbthread = non_blocking_input.KeyboardThread(add_raw_input)
asyncio.get_event_loop().run_until_complete(send_input())