import twisted.internet.defer
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

import gametools

from thing import Thing
from console import Console
from player import Player

from debug import dbg

class NetworkConnection(LineReceiver):
    keep_going = True
    def __init__(self, users):
        self.users = users
        self.user = None
        self.name = None
        self.cons = None
        self.state = "GETNAME"

    def connectionMade(self):
        self.sendLine(b'Username: ')

    def connectionLost(self, reason):
        dbg.debug("ConnectionLost called for %s's connection!" % self.name)
        if self.name in self.users:
            dbg.debug("    Deleting '%s' from self.users dictionary %s" % (self.name, self.users))
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

    def handle_GETNAME(self, namebytes):
        name = str(namebytes, "utf-8")
        if name in self.users:
            self.sendLine(b"Username already in use! Please log on as another user.")
            return
        self.sendLine(b"Welcome, %s!" % (namebytes))
        # if name not in Console.username_to_cons:
        #    self.sendLine(b"There is no user with that username. Would you like to create one?")
        #    self.state = "CONFIRM"
        #    return
        self.cons = Console(self, Thing.game)
        self.user = Player(name, None, self.cons)
        self.cons.user = self.user
        self.user.set_description(name, 'A player named %s' % name)
        self.user.set_max_weight_carried(750000)
        self.user.set_max_volume_carried(2000)

        start_room = gametools.load_room('domains.school.school.great_hall')
        start_room.insert(self.user)

        scroll = gametools.clone('domains.school.scroll')
        scroll.move_to(self.user)
        Thing.game.register_heartbeat(scroll)
        self.user.set_start_loc = start_room
        self.cons.write("\nWelcome to Firlefile Sorcery School!\n\n"
        "Type 'look' to examine your surroundings or an object, "
        "'inventory' to see what you are carrying, " 
        "'quit' to end the game, and 'help' for more information.")


        self.name = name
        self.users[name] = self
        self.state = "COMMAND"

    def handle_COMMAND(self, message):
        self.user.cons.raw_input = message
        dbg.debug("handling user command (user %s, console %s):" % (self.name, self.cons))
        dbg.debug(message)

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
        self.users = {} # maps user names to NetworkConnection instances

    def buildProtocol(self, addr):
        return NetworkConnection(self.users)
