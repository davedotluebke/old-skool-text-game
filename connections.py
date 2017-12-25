''''import twisted.internet.defer
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import os.path
import random

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
        try:
            Thing.game.load_player(os.path.join(gametools.PLAYER_DIR, name), self.cons)
            self.user = self.cons.user
            self.state = "COMMAND"
        except gametools.PlayerLoadError:
            self.create_new_player(name)

    def create_new_player(self, name):
        self.user = Thing.game.create_new_player(name, self.cons)
        self.name = name
        self.users[name] = self
        self.state = "COMMAND"

    def handle_COMMAND(self, message):
        if self.user.cons == None:
            self.transport.loseConnection()
            return
        self.user.cons.raw_input = message



class NetConnFactory(Factory):

    def __init__(self):
        self.users = {} # maps user names to NetworkConnection instances

    def buildProtocol(self, addr):
        return NetworkConnection(self.users)
'''
raise