from action import Action

from thing import Thing
from creature import NPC
from player import Player
from room import Room

class PitRoom(Room):
    def __init__(self, default_name):
        Room.__init__(self, default_name)
        self.set_description('crude pit', 'This is a crude pit. It is about 1/10 filled with water.')
        self.has_player = False
        self.water_level_den = 10
        Thing.ID_dict['nulspace'].game.register_heartbeat(self)
        self.player_done = False

    def heartbeat(self):
        self.has_player = False
        if self.contents:
            for i in self.contents:
                if isinstance(i, Player):
                    self.has_player = True
                    if self.water_level_den > 1:
                        self.water_level_den -= 1
                        self.long_desc = 'This is a crude pit. It is about 1/%s filled with water.' % self.water_level_den
                        i.perceive('The pit fills up more! The water is getting higher faster and faster!')
                    if self.water_level_den == 1 and not self.player_done:
                        self.add_exit('up', Thing.ID_dict['square room'])
                        self.long_desc = 'This is a crude pit. It is completely full of water.'
                        self.player_done = True
                        if i.wizardry_element == 'water':
                            self.ability_realize(i)
                        else:
                            i.die('You cannot breathe, so you die.')
        if not self.has_player:
            self.water_level_den = 10
            self.long_desc = 'This is a crude pit. It is about 1/10 filled with water.'
            try:
                del self.exits['up']
            except KeyError:
                pass
            self.player_done = False
    def ability_realize(self, player):
        player.cons.write('You are now underwater. But you are breathing fine. You begin to realize that you are able to breathe underwater wherever you are.')
        player.cons.write('You feel an urge to find out more about this power, why it exits, and what it does for you.')
        player.cons.write('You notice that now you can reach the trapdoor the goblin closed.')

class Roots(Thing):
    def __init__(self, default_name):
        Thing.__init__(self, default_name)
        self.open = False
        self.set_description('strong roots', 'When you feel theese roots you feel movement and life in them. You feel like you could move them.')
        self.add_adjectives('strong')
        self.actions.append(Action(self.move_roots, ['move'], True, False))
    
    def move_roots(self, p, cons, oDO, oIDO):
        self.open = True
        cons.write('To your suprise, you make the roots part and open up in front of you.')
        cons.write('You feel an urge to find out more about this power, why it exits, and what it does for you.')
        cons.write('You can now go west twords a waterfall.')
        self.location.add_exit('west', Thing.ID_dict['waterfall'])

class MasterGoblin(NPC):
    def __init__(self):
        NPC.__init__(self, 'goblin', Thing.ID_dict['nulspace'].game)
        self.set_description('old mean goblin', 'This goblin is standing straight in front of the passage west. He is holding a piece of paper in his hand.')
        self.add_adjectives('old', 'horrid', 'mean')
        self.add_script('''Listen. If you intend to walk straight past here invisible I tell you that you will not get away with it. 
I am the only one who can let you past and I'm not going to let you get past.
And to pass you must pay me with a gem - an emerald, I think - and give it to me. 
If you do not give me the emerald, however, but keep it, you will be severely punished.''')
        self.pit = PitRoom('pit')
        self.root_room = Room('roots')
        self.root_room.set_description('crude dungeon', 'This is a crude dungeon with a shaft of light coming throgh some tree roots in a corner.')
        self.roots = Roots('roots')
        self.roots.move_to(self.root_room)
        self.complete_players = []
        self.approached = []
        self.complete_message = []
        self.talk_counter = 0
        Thing.ID_dict['nulspace'].game.register_heartbeat(self)

    def heartbeat(self):
        if not self.location:
            return
        for i in self.location.contents:
            if isinstance(i, Player):
                for j in i.contents:
                    if j.names[0] == 'emerald':
                        if i not in self.complete_players:
                            if i.wizardry_element == 'fire':
                                self.throw_fireball(i)
                                return
                            elif i.wizardry_element == 'earth':
                                self.throw_boulder(i)
                                return
                            elif i.wizardry_element == 'water':
                                self.dunk_in_water(i)
                                return
                            elif i.wizardry_element == 'plant':
                                self.throw_in_root_room(i)
                                return
                if i not in self.approached:
                    i.cons.write('The old goblin approaces you.')
                    self.approached.append(i)
                if i not in self.complete_message:
                    self.talk()
                    self.talk_counter += 1
                    if self.talk_counter == 4:
                        self.complete_message.append(i)
                        self.talk_counter = 0
    def throw_fireball(self, player):
        self.emit('The goblin yells "You kept the emerald for yourself! I will punish you!"')
        self.emit('The old goblin makes a fireball in his hands, and prepares to throw it.')
        self.emit('The old goblin throws the fireball at the %s!' % player.short_desc, ignore=[player])
        player.cons.write('The old goblin throws the fireball at you! But for some reason the fireball does not feel hot. It feels warm, and you notice you are not burned.')
        player.cons.write('You feel an urge to find out more about this power, why it exits, and what it does for you.')
        self.emit('The fireball seemingly shatters at %s' % player.short_desc, ignore=[player])
        self.emit('The goblin screams in rage.')
        self.complete_players.append(player)
    
    def throw_boulder(self, player):
        self.emit('The goblin yells "You kept the emerald for yourself! I will punish you!"')
        self.emit('The old goblin picks up a huge rock and prepares to throw it.')
        self.emit('The old goblin throws the huge rock at the %s!' % player.short_desc, ignore=[player])
        player.cons.write('You see a huge boulder flying at you. You instinctively put your hands out in front of you to stop it.')
        self.emit('The %s stops the rock in front of them with their bare hands!' % player.short_desc, ignore = [player])
        player.cons.write('You stop the rock in front of you with just your bare hands!')
        player.strength += 1
        player.cons.write('You feel an urge to find out more about this power, why it exits, and what it does for you.')
        self.emit('The goblin screams in rage.')
        self.complete_players.append(player)

    def dunk_in_water(self, player):
        self.emit('The goblin screams: "You kept the emerald for yourself! I will punish you!"')
        self.emit('The goblin takes %s to a pit.' % player.short_desc, ignore=[player])
        player.cons.write('The goblin opens a trap door below you to a pit and you fall in. You land in water at the bottom of the pit. Unfortunately, it seems it is slowly getting higher and higher.')
        player.move_to(self.pit)
        self.emit('The goblin says "They will die! Ha Ha Ha!"')
        self.complete_players.append(player)

    def throw_in_root_room(self, player):
        self.emit('The goblin screams: "You kept the emerald for yourself! I will punish you!"')
        self.emit('The goblin throws %s in a dungeon room.' % player.short_desc)
        player.cons.write('The goblin throws you into a dungeon room. You see light through a wall covered in tree roots, but no way out.')
        player.move_to(self.root_room)
        self.emit('The goblin says "They will sit there for a long time! Ha Ha Ha!"')
        self.complete_players.append(player)
