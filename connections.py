import twisted.internet.defer
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

from thing import Thing
from console import Console

class NetworkConnection(LineReceiver):

    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = "GETNAME"
        self.setLineMode()

    def connectionMade(self):
        self.sendLine(b'Username: ')

    def connectionLost(self, reason):
        if self.name in self.users:
            del self.users[self.name]

    def lineReceived(self, line):
        if self.state == "GETNAME":
            self.handle_GETNAME(line)
        elif self.state == "CONFIRM":
            self.handle_CONFIRM(line)
        elif self.state == "CREATE":
            self.handle_CREATE(line)
        else:
            self.handle_COMMAND(line)

    def handle_GETNAME(self, name):
        if name in self.users:
            self.sendLine(b"Username already in use! Please log on as another user.")
            return
        print(name)
        print(Console.username_to_cons)
        if name not in Console.username_to_cons:
            self.sendLine(b"There is no user with that username. Would you like to create one?")
            self.state = "CONFIRM"
            return
        self.cons = Console.username_to_cons[name]
        self.cons.connection = self
        self.sendLine(b"Welcome, %s!" % (name,))
        self.name = name
        self.users[name] = self
        self.state = "COMMAND"

    def handle_COMMAND(self, message):
        g = Thing.game
        g.cons.raw_input = message

 #       message = b"<%s> %s" % (self.name, message)
 #       for name, protocol in self.users.items():
 #           if protocol != self:
 #               protocol.sendLine(message)
    
    def handle_CONFIRM(self, confirm):
        if confirm.lower() != b'yes':
            self.sendLine(b"Not creating a new user. Type a username to log in.")
            self.state = "GETNAME"
            return
        self.sendLine(b"New username: ")
        self.state = "CREATE"
    
    def handle_CREATE(self, username):
        self.username = username
        self.name = username
        self.users[username] = self
        self.state = "COMMAND"


class NetConnFactory(Factory):

    def __init__(self):
        self.users = {} # maps user names to Chat instances

    def buildProtocol(self, addr):
        return NetworkConnection(self.users)

#XXX not sure how to use deffereds with reactor
class DefferedReactor(reactor):
    def run():
        d = twisted.internet.defer.Deferred()
        super().run()

DefferedReactor.listenTCP(9123, NetConnFactory())
DefferedReactor.run()
