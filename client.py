import socket
import sys
import readline

class Client:
    # Connect to server 
    HOST, PORT = "localhost", 9999
    data = " ".join(sys.argv[1:])  # eventually use this to specify host and port
    print(data)
    def loop(self):
        self.command = ''
        cmd = ''
        received_p_data = True
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

            while received.rfind('__parser__') != -1:
                (head, sep, tail) = received.partition('__parser__')
                received = head + tail
                received_p_data = True

            sys.stdout.write(received)

            # shut down
            sock.close()
            if self.command == 'quit':
                break

            if not received_p_data:
                continue

            char = sys.stdin.read(1)            
            if char == '\n':
                self.command = cmd
                cmd = ''
                received_p_data = False
            else:
                cmd += char
                char = ''
                self.command = ''

c = Client()
c.loop()
