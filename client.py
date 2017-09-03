import socket
import sys

HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])  # eventually use this to specify host and port 

# Connect to server 

while True:
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    command = input('---> ')

    sock.send(bytes(command + "\n", "utf-8"))

    # Receive data from the server and shut down
    received_bytes = sock.recv(1024)
    received = str(received_bytes, "utf-8")
    print("Sent:     {}".format(command))
    print("Received: {}".format(received))
    sock.close()
    if command == 'quit':
        break
    
