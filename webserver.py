from twisted.web import server, resource
from twisted.internet import reactor, endpoints
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet.threads import deferToThread

import html

class SendToWeb(Protocol):
    data = ''
    toSend = ''
    def dataReceived(self, data):
        SendToWeb.data = data
        if Simple.item_to_send_lines == None:
            Simple.item_to_send_lines = self

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
        return bytes("<html>" + str(SendToWeb.data,"utf-8") + "<form method='POST'><input type='text' name='line_to_send'></form></html>","utf-8")
    def render_POST(self, request):
        try:
            SendToWeb.toSend = (request.args[b"line_to_send"][0])
        except KeyError:
            pass
        Simple.item_to_send_lines.transport.write(SendToWeb.toSend,)
        return bytes("<html>Handled. Waiting for server...</html>","utf-8")

site = server.Site(Simple())
endpoint = endpoints.TCP4ServerEndpoint(reactor, 9124)
endpoint.listen(site)
reactor.connectTCP("localhost", 9123, SendToWebFactory())
reactor.run()

