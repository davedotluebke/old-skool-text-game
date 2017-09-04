import socket
import sys

class Client:
    # Connect to server 
    HOST, PORT = "localhost", 9999
    data = " ".join(sys.argv[1])  # eventually use this to specify host and port
    print(data)
    def loop(self):
        self.command = ''
        while True:
            # Create a socket (SOCK_STREAM means a TCP socket)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((Client.HOST, Client.PORT))

            # Send data from input
            sending = bytes(self.command + "\n", "utf-8")
            sock.send(sending)
            
            # Receive data from the server
            received_bytes = sock.recv(1024)
            received = str(received_bytes, "utf-8")
            print(received)

            # shut down
            sock.close()
            if self.command == 'quit':
                break
            
            self.command = input('-> ')

c = Client()
c.loop()
