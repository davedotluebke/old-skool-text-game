import creature
import player
import gametools

class Bat(creature.NPC):
    def __init__(self):
        super().__init__('bat', __file__, aggressive=2)
        self.set_description('vicious bat', 'This is a vicious-looking vampire bat. It has bright red eyes.')
        self.add_adjectives('vicious', 'vampire', 'red-eyed')
        self.choices = [self.attack_enemy]
        self.set_combat_vars(30, 40, 3, 87)
        self.default_weapon = gametools.clone('domains.centrata.firefile_area.key_quest.bat_bite')
        self.weapon_wielding = self.default_weapon
        self.introduction_complete = False
        self.new_bat_counter = 0
    
    def have_key(self):
        first_key = gametools.clone('domains.centrata.firefile_area.key_quest.key')
        first_key.qkey_number = 1
        self.insert(first_key)

    def heartbeat(self):
        if not self.location:
            return
        for i in self.location.contents:
            if isinstance(i, player.Player):
                if not self.introduction_complete:
                    self.emit('The vampire bat flies up through the gap in the ceiling, and dives back down at you.')
                    self.introduction_complete = True
                self.attack_enemy()
        self.new_bat_counter += 1
        if self.new_bat_counter == 5:
            self.emit('A new bat arrives!')
            new_bat = gametools.clone(gametools.findGamePath(__file__))
            new_bat.move_to(self.location, True)
            new_bat_counter = 0
        else:
            self.introduction_complete = False

def clone():
    return Bat()
