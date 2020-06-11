import creature
import gametools
import random

class ProfSun(creature.NPC):
    rubies_powered = []
    def __init__(self):
        super().__init__('profsun', __file__)
        self.set_description('tall wise elf', 'This is a tall, wise elf.')
        self.add_names('sun', 'elf')
        self.add_adjectives('mr')
        self.graduates = []
        self.waiting = False
        self.unchecked_homework = []
        self.wizardry_element = 'fire'
        self.proper_name = 'Prof. Sun'
        self.giving_class = False
        self.script_index = 0
        self.scripts = ['''Magical gems are foundational to the art of wizardry. Their role on society is unchallenged.
        There are three basic types of gems: the producers, the connecters, and the consumers.
        The producers are essential, as they store all power. The most common producer is emerald.
        The connecters are essential to  long distance communictions. The most common connecter is jade.
        Finally, the consumers are the gems that bring us light and wampth, sound and flight. The most common consumer is hard to say, although it might be ruby.
        Now you will perform an experiment in basic gem connection. I will give each of you an emerald and a ruby. You shall power the ruby using the power from the emerald. When you do, it will make light.''',
        '''Very good job.
        Your homework will be to power an opal with an emerald to make dark.''']
        self.emeralds = [gametools.clone('domains.school.school.emerald')]
        self.rubies = [gametools.clone('domains.school.school.ruby')]
        self.checking_done = False
        self.resetting = False
        
    def heartbeat(self):
        # If waiting on something, then return
        if self.waiting:
            return

        # If checking status, continue
        if self.checking_done:
            self.check()
            return
        
        # If giving a class, continue
        if self.giving_class:
            self.give_class()
            return

        # If checking homework, continue
        if self.unchecked_homework:
            i = self.unchecked_homework[0]
            if i == self:
                del self.unchecked_homework[0]
            elif i.wizardry_element == None:
                self.emit('Prof. Sun says: %s, you have come to the wrong class. Your scroll should inform you of when your class starts. See you then.' % i)
                self.emit('&nD%s vanishes!' % i.id)
                dest = gametools.load_room('domains.school.school.library')
                i.move_to(dest)
                dest.report_arrival(i)
                del self.unchecked_homework[0]
            else:
                self.emit('Prof. Sun says: %s, you are good to go.' % i.proper_name)
                del self.unchecked_homework[0]
            if not self.unchecked_homework:
                self.emit('Prof. Sun says: Okay, we are good to go.')
                self.begin_class()
            return

        # Otherwise, check to see if there are any players in the room
        players = [x for x in self.location.contents if isinstance(x, creature.Creature) and x not in self.graduates and x != self]
        if not players:
            return

        # If there are players, check their homework
        self.emit('The tall, wise elf says: Hello. I am Prof. Sun. Welcome to my class.\nI will begin by checking your homework.')
        self.unchecked_homework = players

    def begin_class(self):
        self.emit('Prof. Sun says: Today we will be discussing the usage of magical gems.')
        self.current_script = self.scripts[0]
        self.script_index = 0
        self.giving_class = True

    def give_class_ev(self):
        self.give_class()

    def give_class(self):
        lines = self.current_script.splitlines()
        index = self.current_script_idx
        if index >= len(lines):
            self.do_action()
            if not self.resetting:
                self.current_script = self.scripts[self.script_index]
            return
        self.emit('Prof. Sun says: '+lines[index])
        self.waiting = True
        creature.Thing.game.schedule_event(15, self.give_class_ev)
        self.current_script_idx += 1

    def present_gems(self):
        players = [x for x in self.location.contents if isinstance(x, creature.Creature) and x not in self.graduates and x != self]
        while len(players) > len(self.emeralds):
            self.emeralds.append(gametools.clone('domains.school.school.emerald'))
            self.rubies.append(gametools.clone('domains.school.school.ruby'))
        for i in range(0, len(players)):
            self.emeralds[i].move_to(players[i])
            self.rubies[i].move_to(players[i])
            players[i].perceive('You notice an emerald and a ruby appear in front of you.')
        self.waiting = False
        self.checking_done = True

    def check(self):
        if len(ProfSun.rubies_powered) == len([x for x in self.location.contents if isinstance(x, creature.Creature) and x not in self.graduates and x != self]):
            self.checking_done = False
            for i in self.emeralds:
                i.move_to(self, True)
            for i in self.rubies:
                i.move_to(self, True)
            ProfSun.rubies_powered = []
            self.emit('Prof. Sun says: It seems you all understand.')

    def do_action(self):
        self.waiting = True
        if self.script_index == 0:
            self.present_gems()
        elif self.script_index == 1:
            creature.Thing.game.schedule_event(80, self.reset, None)
            self.resetting = True
        self.script_index += 1
        self.current_script_idx = 0

    def reset(self):
        self.graduates += [x for x in self.location.contents if isinstance(x, creature.Creature) and x not in self.graduates and x != self]
        self.waiting = False
        self.script_index = 0
        self.current_script_idx = 0
        self.checking_done = False
        self.current_script = self.scripts[0]
        self.giving_class = False
        ProfSun.rubies_powered = []
        self.resetting = False

def clone():
    return ProfSun()
