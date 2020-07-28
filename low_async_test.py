import asyncio
import functools
import sys

main_protocol = None

class BashCommunicationProtocol(asyncio.SubprocessProtocol):
    def __init__(self, exit_future):
        self.exit_future = exit_future
        self.output = bytearray()

    def pipe_data_received(self, fd, data):
        self.fd = fd
        print(data.decode('utf-8'))
        self.output.extend(data)
    
    def send_input(self, input):
        self.transport.get_pipe_transport(self.fd).write(input.encode('utf-8'))

    def process_exited(self):
        self.exit_future.set_result(True)

async def get_date():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_event_loop()

    exit_future = asyncio.Future(loop=loop)

    # Create the subprocess controlled by DateProtocol;
    # redirect the standard output into a pipe.
    transport, protocol = await loop.subprocess_exec(
        lambda: BashCommunicationProtocol(exit_future),
        'bash',
        stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    
    protocol.transport = transport
    print(dir(transport))

    global main_protocol
    main_protocol = protocol
    
    # Wait for the subprocess exit using the process_exited()
    # method of the protocol.
    await exit_future

    # Close the stdout pipe.
    transport.close()

    # Read the output which was collected by the
    # pipe_data_received() method of the protocol.
    data = bytes(protocol.output)
    return data.decode('ascii').rstrip()

def add_input_to_process():
    main_protocol.send_input(input('_'))

asyncio.get_event_loop().call_later(2, add_input_to_process)
date = asyncio.get_event_loop().run_until_complete(get_date())
print(f"Current date: {date}")