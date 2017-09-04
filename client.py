import socket
import sys

HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])  # eventually use this to specify host and port 

# Connect to server 

while True:
    command = input('-> ')

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    # Send data from input
    sending = bytes(command + "\n", "utf-8")
    sock.send(sending)

    print("Sending Command: {}".format(command))
    print("Command Byte Value: {}".format(sending))

    # Receive data from the server
    received_bytes = sock.recv(1024)
    received = str(received_bytes, "utf-8")
    print(received)

    # shut down
    sock.close()
    if command == 'quit':
        break
    
