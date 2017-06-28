from debug import dbg

from thing import Thing
from container import Container
from room import Room
from action import Action
from creature import Creature
from player import Player
from creature import NPC

monster = NPC('monster', Thing.ID_dict['nulspace'].game, 2)
monster.set_description('terrible monster', 'This is a horrible monster. You want to run away from it.')
monster.set_combat_vars(50, 60, 80, 40)
monster.act_frequency = 1
monster.set_volume(100)
monster.set_weight(500000)

class Lair(Room):
    def go_to(self, p, cons, oDO, oIDO):
        if self.monster in self.contents:
            if p.words[1] == 'northwest':
                if cons.user.invisible != True:
                    cons.write('You try to enter the crawlway, but the monster blocks your path.')
                    return True
        return Room.go_to(self, p, cons, oDO, oIDO)

lair = Lair('lair')
lair.set_description('monster\'s lair', 'This is a lair where the terrible monster hides. It has a wall with clubs hanging on it. There is a crawlway to the northwest.')
lair.add_adjectives("monster's")

class CaveRoom(Room):
    def __init__(self, ID):
        Room.__init__(self, ID, light=0)
        self.monster_storage = lair
        self.released_monster = False
        self.create_cave_moss()
        self.create_gold()

    def create_cave_moss(self):
        for i in self.contents:
            if i.names[0] == 'cave moss':
                return True
        cave_moss = Thing('cave moss')
        cave_moss.set_description('cave moss', 'This is some strange moss growing in the cave.')
        cave_moss.add_adjectives('cave')
        cave_moss.add_names('moss')
        cave_moss.move_to(self)

    def create_gold(self):
        for i in self.contents:
            if i.names[0] == 'gold':
                return True
        gold = Thing('gold')
        gold.set_description('bunch of shiny gold coins', 'This is a collection of seven shiny real gold coins.')
        gold.set_weight(74000)
        self.insert(gold)
    
    def attach_monster(self, monster):
        self.monster = monster
        del self.monster.choices[0]  #keeps monster from moving around except to attack people in the cave or lair
        del self.monster.choices[1]  #so the monster is quicker to choose the attack_enemy option. TODO: make monster automatically attack enemy when it is released.
        self.monster.move_to(self.monster_storage)
        self.monster_storage.monster = self.monster
    
    def go_to(self, p, cons, oDO, oIDO):
        if self.monster in self.contents:
            if p.words[1] == 'west':
                if cons.user.invisible != True:
                    cons.write('You try to go to the west, but the monster blocks your path.')
                    return True
        return Room.go_to(self, p, cons, oDO, oIDO)

    def heartbeat(self):
        gold_check = False
        cave_moss_check = False
        for k in self.contents:
            if k.names[0] == 'cave moss':
                cave_moss_check = True
            if k.names[0] == 'gold':
                gold_check = True
        if not cave_moss_check or not gold_check:
            if self.released_monster == False:
                if self.monster.location == self.monster_storage:
                    self.monster_storage.extract(self.monster)
                    self.insert(self.monster)
                    self.monster.emit('A %s arrives!' % self.monster.short_desc)
                    self.released_monster == True
                    self.counter = 10
                    for m in self.contents:
                        if m != self.monster and isinstance(m, Creature):
                            self.monster.enemies.append(m)
        if self.released_monster:
            self.counter -= 1
            if self.counter <= 0:
                self.monster.move_to(self.monster_storage)
                self.create_cave_moss()
                self.create_gold()
                self.released_monster = False

cave = CaveRoom('cave')
cave.set_description('terrifying dark cave', 'This is one of the most scary caves you have ever been in. You are anxiousley looking around to see if there are any monsters.')
cave.add_adjectives('scary', 'dark', 'terrifying')

class CaveEntry(Room):
    def __init__(self, ID):
        Room.__init__(self, ID)
        self.set_description('terrifying dark cave mouth', 'This is one of the most scary caves you have ever been seen. You are anxiously looking around to see if there are any monsters.')
        self.add_adjectives('scary', 'dark', 'terrifying')
        self.in_entry_user = 0
        self.last_cons = None
    
    def add_aditional_vars(self, escape_room, g):
        self.escape_room = escape_room
        g.register_heartbeat(self)
        self.game_redirect = g
   
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
            dbg.debug(str(self.in_entry_user))
        elif self.in_entry_user > 0 and contents_question:
            for i in self.contents:
                if isinstance(i, Player):
                    i.cons.write('You step back from the cave mouth into the gloomy forest.')
                dbg.debug('extracting %s!' % i)
                self.extract(i)
                self.escape_room.insert(i)
            self.in_entry_user = 0
#        if (Thing.ID_dict['cave moss'] or Thing.ID_dict['gold']) not in self.exits['in'].contents:

cave_entrance = CaveEntry('cave mouth')
lair.add_exit('east', cave)
lair.add_exit('northwest', Thing.ID_dict['crawlway'])
cave.add_exit('west', lair)
cave_entrance.add_exit('in', cave)
cave.attach_monster(monster)
