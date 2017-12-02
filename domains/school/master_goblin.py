from action import Action
import gametools

from thing import Thing
from creature import NPC
from player import Player
from room import Room

class PitRoom(Room):
    def __init__(self, default_name, pref_id):
        Room.__init__(self, default_name, pref_id=pref_id)
        self.set_description('crude pit', 'This is a crude pit. It is about 1/10 filled with water.')
        self.indoor = True
        self.has_player = False
        self.water_level_den = 10
        Thing.game.register_heartbeat(self)
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
                        self.add_exit('up', 'waterfall')
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
        player.cons.write('You feel an urge to find out more about this power, why it exists and what it does for you.')
        player.cons.write('You notice that now you can reach the trapdoor the goblin closed.')

class Roots(Thing):
    def __init__(self, default_name, path):
        Thing.__init__(self, default_name, path)
        self.open = False
        self.set_description('strong roots', 'These roots look very strong. You wish you could move them.')
        self.add_adjectives('strong')
        self.actions.append(Action(self.move_roots, ['move'], True, False))
    
    def move_roots(self, p, cons, oDO, oIDO):
        if cons.user.wizardry_element == 'plant':
            self.open = True
            cons.write('To your surprise, when you put your hands on the roots you find you can make them part and open up in front of you.')
            cons.write('You feel an urge to find out more about this power, why it exists and what it does for you.')
            cons.write('You can now go west towards a waterfall.')
            self.location.add_exit('west', 'waterfall')
            return True
        else:
            cons.write("You can't move the roots, they're very strong!")
            return True

class MasterGoblin(NPC):
    def __init__(self, path):
        NPC.__init__(self, 'goblin', path, Thing.ID_dict['nulspace'].game)
        self.set_description('old mean goblin', 'This goblin is standing straight in front of the passage west. He is holding a piece of paper in his hand.')
        self.add_adjectives('old', 'horrid', 'mean')
        self.add_script('''Listen. If you intend to walk straight past here invisible, I tell you that you will not get away with it.
I am the only one who can let you past and I'm not going to let you get past.
And to pass you must acquire a gem--an emerald, I think--and give it to me.
If you do not give me the emerald, however, but keep it, you will be severely punished.''')
        self.pit = gametools.load_room('domains.school.dungeon.pit')
        self.root_room = gametools.load_room('domains.school.dungeon.root_room')
        self.roots = gametools.clone('domains.school.dungeon.roots')
        self.complete_players = []
        self.approached = []
        self.complete_message = []
        self.talk_counter = 0
        Thing.game.register_heartbeat(self)

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
                            elif i.wizardry_element == 'air':
                                self.throw_in_root_room(i)
                                return
                if i not in self.approached:
                    i.cons.write('The old goblin approaches you.')
                    self.approached.append(i)
                if i not in self.complete_message:
                    self.talk()
                    self.talk_counter += 1
                    if self.talk_counter == 4:
                        self.complete_message.append(i)
                        self.talk_counter = 0
    def throw_fireball(self, player):
        self.emit('The goblin yells, "You kept the emerald for yourself! I will punish you!"')
        self.emit('The old goblin makes a fireball in his hands, and prepares to throw it.')
        Thing.game.events.schedlue(Thing.game.time+2, self.throw_fireball_two, player)

    def throw_fireball_two(self, player):
        self.emit('The old goblin throws the fireball at the %s!' % player.short_desc, ignore=[player])
        player.cons.write('The old goblin throws the fireball at you! But for some reason the fireball does not feel hot. It feels warm, and you notice you are not burned.')
        self.emit('The fireball seemingly shatters at %s' % player.short_desc, ignore=[player])
        Thing.game.events.schedlue(Thing.game.time+2, self.throw_fireball_three, player)

    def throw_fireball_three(self, player):
        self.emit('The goblin smiles. "Correct! A new fire wizard!"')
        player.cons.write('The goblin says to you, "Congratulations on becoming a fire wizard. It shall serve you well."')
        self.complete_players.append(player)
        player.cons.write('The goblin motions for you to walk past him.')
        player.move_to(Thing.ID_dict['domains.school.forest.crimpson'])
    
    def throw_boulder(self, player):
        self.emit('The goblin yells, "You kept the emerald for yourself! I will punish you!"')
        self.emit('The old goblin picks up a huge rock and prepares to throw it.')
        Thing.game.events.schedlue(Thing.game.time+2, self.throw_boulder_two, player)

    def throw_boulder_two(self, player):
        self.emit('The old goblin throws the huge rock at the %s!' % player.short_desc, ignore=[player])
        player.cons.write('You see a huge boulder flying at you. You instinctively put your hands out in front of you to stop it.')
        self.emit('The %s stops the rock in front of them with their bare hands!' % player.short_desc, ignore = [player])
        player.cons.write('You stop the rock in front of you with just your bare hands!')
        player.strength += 1
        Thing.game.events.schedlue(Thing.game.time+2, self.throw_boulder_three, player)

    def throw_boulder_three(self, player):
        self.emit('The goblin smiles. "Correct! A new earth wizard!"')
        player.cons.write('The goblin says to you, "Congratulations on becoming an earth wizard. It shall serve you well."')
        self.complete_players.append(player)
        player.cons.write('The goblin motions for you to walk past him.')
        player.move_to(Thing.ID_dict['domains.school.forest.crimpson'])

    def dunk_in_water(self, player):
        self.emit('The goblin screams, "You kept the emerald for yourself! I will punish you!"')
        self.emit('The goblin takes %s to a pit.' % player.short_desc, ignore=[player])
        player.cons.write('The goblin opens a trapdoor below you to a pit and you fall in. You land in water at the bottom of the pit. Unfortunately, it seems it is slowly getting higher and higher.')
        player.move_to(self.pit)
        self.emit('The goblin says "They will die! Ha Ha Ha!"')
        self.complete_players.append(player)

    def throw_in_root_room(self, player):
        self.emit('The goblin screams, "You kept the emerald for yourself! I will punish you!"')
        self.emit('The goblin throws %s in a dungeon room.' % player.short_desc)
        player.cons.write('The goblin throws you into a dungeon room. You see light through a wall covered in tree roots but no way out.')
        player.move_to(self.root_room)
        self.emit('The goblin says, "They will sit there for a long time! Ha Ha Ha!"')
        self.complete_players.append(player)

    def move_player_to_waterfall(self, player):
        player.cons.write("All of a sudden the world shifts around you. The dark walls of the room blur into green and blue. They start fading into something. You start sliding forward.")
        player.move_to(Thing.ID_dict['waterfall'])
        Thing.ID_dict['waterfall'].report_arrival(player)
