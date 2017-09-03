import socketserver
import time

class MyTCPHandler(socketserver.StreamRequestHandler):
    '''
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

    '''        
    quit_soon = False
    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        if str(self.data, "utf-8").strip() == "quit":
            MyTCPHandler.quit_soon = True
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        print("writing %s back" % self.data.upper())
        self.wfile.write(self.data.upper())

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    
    num = 0
    while True:
        num += 1
        server.handle_request()
        print('handled request # %s' % num)
        time.sleep(1)
        if MyTCPHandler.quit_soon:
            print("quitting now")
            break
    server.server_close()
