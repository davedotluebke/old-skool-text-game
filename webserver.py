from twisted.web import server, resource
from twisted.internet import reactor, endpoints
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet.threads import deferToThread
from twisted.conch.recvline import HistoricRecvLine

import html

class SendToWeb(Protocol):
    data = ''
    toSend = ''
    def dataReceived(self, data):
        print(data)
        SendToWeb.data = data
        if Simple.item_to_send_lines == None:
            Simple.item_to_send_lines = self
        

    def sendData_fuction(self):
        print(SendToWeb.toSend)
        self.transport.write(SendToWeb.toSend + b'\r\n')
        SendToWeb.toSend = ''
        print(SendToWeb.toSend)

class SendToWebFactory(ReconnectingClientFactory):
    def startedConnecting(self, connector):
        print('Started to connect.')

    def buildProtocol(self, addr):
        print('Connected.')
        print('Resetting reconnection delay')
        self.resetDelay()
        return SendToWeb()

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.  Reason:', reason)
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason)
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

class Simple(resource.Resource):
    isLeaf = True
    item_to_send_lines = None
    def render_GET(self, request):
        return bytes("<html>" + str(SendToWeb.data,"utf-8").replace('\n', '<br>') + "<form method='POST'><input type='text' name='line_to_send'></form></html>","utf-8")
    def render_POST(self, request):
        SendToWeb.toSend = (request.args[b"line_to_send"][0])
        if SendToWeb.toSend == b'__donotsend__':
            SendToWeb.toSend = ''
            return bytes("<html>" + str(SendToWeb.data,"utf-8").replace('\n', '<br>') + "<form method='POST'><input type='text' name='line_to_send'></form></html>","utf-8")
        Simple.item_to_send_lines.sendData_fuction()
        return bytes("<html>Handled. Waiting for server...<form method='POST'><input type='hidden' value='__donotsend__' name='line_to_send'><button>Check for response</button></html>","utf-8")

site = server.Site(Simple())

def setup(port):
    endpoint = endpoints.TCP4ServerEndpoint(reactor, port)
    endpoint.listen(site)
    reactor.connectTCP("localhost", 9123, SendToWebFactory())

def run():
    reactor.run()
