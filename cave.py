from debug import dbg

from thing import Thing
from container import Container
from room import Room
from action import Action

class CaveEntry(Room):
    def __init__(self, ID, escape_room, g):
        Room.__init__(self, ID)
        self.set_description('terrifying dark cave mouth', 'This is one of the most scary caves you have ever been seen. You are anxiously looking around to see if there are any monsters.')
        self.add_adjectives('scary', 'dark', 'terrifying')
        self.in_entry_user = 0
        self.escape_room = escape_room
        g.register_heartbeat(self)
        self.game_redirect = g
        self.last_cons = None
   
    def go_to(self, p, cons, oDO, oIDO):
        try:
            if p.words[1] == 'east':
                Room.go_to(self, p, cons, oDO, oIDO)
            elif cons == self.last_cons:
                if cons != None:
                    self.last_cons = cons
                cons.write('You convince yourself to enter the scary cave.')
                cons.user.emit('%s slowly enters the cave, visibly shaking.' % cons.user.names[0])
                Room.go_to(self, p, cons, oDO, oIDO)
                dbg.debug('%s slowly enters the cave, visibly shaking. The DebugLog says that the cave is scary, because it was meant to be.' % cons.user.id)
            else:
                cons.write('Entering the cave is very scary, and you have a hard time convincing yourself to go in.')
                if cons != None:
                    self.last_cons = cons
                    dbg.debug('self.last_cons was just set to %s, %s' % (self.last_cons, cons))
        except AttributeError:
            cons.write('Entering the cave is very scary, and you have a hard time convincing yourself to go in.')
            if cons != None:
                self.last_cons = cons
                dbg.debug('self.last_cons was just set to %s, %s' % (self.last_cons, cons))
   
    def heartbeat(self):
        dbg.debug('self.last_cons is %s' % self.last_cons)
        try:
            test_var = self.contents[0].id
            dbg.debug(test_var)
            contents_question = True
        except IndexError:
            contents_question = False
            dbg.debug('Nothing in the CaveEntry')
        dbg.debug("%s, %s" % (contents_question, self.in_entry_user))
        if self.in_entry_user < 1 and contents_question:
            self.in_entry_user += 1
            dbg.debug(self.in_entry_user)
        elif self.in_entry_user > 0 and contents_question:
            for i in self.contents:
                if i == self.game_redirect.user:
                    self.game_redirect.cons.write('You step back from the cave mouth into the gloomy forest.')
                dbg.debug('extracting %s!' % i)
                self.extract(i)
                self.escape_room.insert(i)
            self.in_entry_user = 0                
