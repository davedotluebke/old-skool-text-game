from debug import dbg

from thing import Thing
from container import Container
from room import Room
from action import Action
from creature import Creature

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
        self.released_monster = False
        self.monster_storage = Room('monster_storage073T4', 0)
        self.create_cave_moss()
        self.create_gold()

    def create_cave_moss(self):
        try:
            if Thing.ID_dict['moss'] not in self.exits['in'].contents:
                cave_moss = Thing('cave moss')
                cave_moss.set_description('cave moss', 'This is some strange moss growing in the cave.')
                cave_moss.add_adjectives('cave')
                cave_moss.add_names('moss')
                cave_moss.move_to(self.exits['in'])
        except KeyError:
                cave_moss = Thing('cave moss')
                cave_moss.set_description('cave moss', 'This is some strange moss growing in the cave.')
                cave_moss.add_adjectives('cave')
                cave_moss.add_names('moss')
                cave_moss.move_to(Thing.ID_dict['cave'])

    def create_gold(self):
        try:
            if Thing.ID_dict['gold'] not in self.exits['in'].contents:
                gold = Thing('gold')
                gold.set_description('bunch of shiny gold coins', 'This is a collection of seven shiny real gold coins.')
                gold.set_weight(74000)
                self.exits['in'].insert(gold)
        except KeyError:
            gold = Thing('gold')
            gold.set_description('bunch of shiny gold coins', 'This is a collection of seven shiny real gold coins.')
            gold.set_weight(74000)
            Thing.ID_dict['cave'].insert(gold)
    
    def attach_monster(self, monster):
        self.monster = monster
        self.monster.move_to(self.monster_storage)
   
    def go_to(self, p, cons, oDO, oIDO):
        if p.words[1] == 'east':
            return Room.go_to(self, p, cons, oDO, oIDO)
        elif cons == self.last_cons:
            if cons != None:
                self.last_cons = cons
            cons.write('You convince yourself to enter the scary cave.')
            cons.user.emit('%s slowly enters the cave, visibly shaking.' % cons.user)
            Room.go_to(self, p, cons, oDO, oIDO)
            dbg.debug('%s slowly enters the cave, visibly shaking. The DebugLog says that the cave is scary, because it was meant to be.' % cons.user.id)
            return True
        else:
            cons.write('Entering the cave is very scary, and you have a hard time convincing yourself to go in.')
            if cons != None:
                self.last_cons = cons
                dbg.debug('self.last_cons was just set to %s, %s' % (self.last_cons, cons))
            return True
   
    def heartbeat(self):
        dbg.debug('self.last_cons is %s' % self.last_cons)
        try:
            self.contents[0].id
            dbg.debug('contents[0] of cave is %s' % self.contents[0].id)
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
#        if (Thing.ID_dict['cave moss'] or Thing.ID_dict['gold']) not in self.exits['in'].contents:
        gold_check = False
        cave_moss_check = False
        for k in self.exits['in'].contents:
            if k.names[0] == 'cave moss':
                cave_moss_check = True
            if k.names[0] == 'gold':
                gold_check = True
        if not cave_moss_check or not gold_check:
            if self.released_monster == False:
                if self.monster.location == self.monster_storage:
                    self.monster_storage.extract(self.monster)
                    self.exits['in'].insert(self.monster)
                    self.monster.emit('A %s arrives!' % self.monster.short_desc)
                    self.released_monster == True
                    self.counter = 10
                    for m in self.monster.location.contents:
                        if m != self.monster and isinstance(m, Creature):
                            self.monster.enemies.append(m)
        if self.released_monster:
            self.counter -= 1
            if self.counter <= 0:
                self.monster.move_to(self.monster_storage)
                self.create_cave_moss()
                self.create_gold()
                self.released_monster = False
