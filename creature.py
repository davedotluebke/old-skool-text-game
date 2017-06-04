import random
from debug import dbg
from thing import Thing
from container import Container
from weapon import Weapon
from armor import Armor

class Creature(Container):
    def __init__(self, default_name, pref_id=None):
        Container.__init__(self, default_name, pref_id)
        self.closed = True
        self.closable = False
        self.see_inside = False
        self.hitpoints = 10           # default hitpoints
        self.health = self.hitpoints  # default full health (0 health --> dead)
        self.enemies = []
        self.viewed = False
        self.armor_class = 0
        self.combat_skill = 0
        self.strength = 0
        self.dexterity = 1
        self.default_weapon = Weapon("bare hands", 1, 5, 1)
        self.default_armor = Armor("skin", 0, 0)
        self.weapon_wielding = self.default_weapon
        self.armor_worn = self.default_armor
        self.closed_err = "You can't put things in creatures!"
        self.visible_inventory = []     #Things the creature is holding, you can see them.
        self.invisible = False

    def set_default_weapon(self, name, damage, accuracy, unwieldiness):
        self.default_weapon = Weapon(name, damage, accuracy, unwieldiness)
    def set_default_armor(self, name, bonus, unwieldiness):
        self.default_armor = Armor(name, bonus, unwieldiness)

    def set_combat_vars(self, armor_class, combat_skill, strength, dexterity):
        self.armor_class = armor_class
        self.combat_skill = combat_skill
        self.strength = strength
        self.dexterity = dexterity

    def look_at(self, p, cons, oDO, oIDO):
        '''Print out the long description of the creature, as well as any Weapons it is wielding and any armor it is wearing.'''
        self.viewed = cons.user
        dbg.debug("Called Creature.look_at()")
        if self == oDO or self == oIDO:
            cons.write(self.long_desc)
            if self.weapon_wielding:
                cons.write("It is wielding a %s." % (self.weapon_wielding.short_desc))        #if we use "bare hands" we will have to change this
            if self.armor_worn:
                cons.write("It is wearing %s." % (self.armor_worn.short_desc))
            if self.visible_inventory and self.visible_inventory != [self.armor_worn, self.weapon_wielding] and self.visible_inventory != [self.weapon_wielding, self.armor_worn]:
                cons.write('It is holding:')
                for i in self.visible_inventory:
                    if i != self.armor_worn and i != self.weapon_wielding:
                        cons.write('/na '+i.short_desc)
            return True
        else:
            return "Not sure what you are trying to look at!"

    def perceive(self, message):
        """Receive a message emitted by an object carried by or in vicinity of this creature."""
        dbg.debug("perceived a message "+message+" in Creature.perceive()")

    def say(self, speech):
        """Emit a message to the room "The <creature> says: <speech>". """
        self.emit("The %s says: %s" % (self, speech))

    def get_armor_class(self):
        return self.armor_class + (0 if not self.armor_worn else self.armor_worn.bonus)
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die('default message')

    def weapon_and_armor_grab(self):
        if not self.weapon_wielding:
            for w in self.contents:
                if isinstance(w, Weapon):
                    self.weapon_wielding = w
                    dbg.debug("weapon chosen: %s" % self.weapon_wielding)
                    self.visible_inventory.append(self.weapon_wielding)
                    break
        if not self.armor_worn:
            for a in self.contents:
                if isinstance(a, Armor):
                    self.armor_worn = a
                    dbg.debug("armor chosen: %s" % self.armor_worn)
                    self.visible_inventory.append(self.armor_worn)
                    break

    def attack(self, enemy):
        if (self == enemy):
            dbg.debug('Creature tried to attack self!')
            return
        chance_of_hitting = self.combat_skill + self.weapon_wielding.accuracy - enemy.get_armor_class()
        if random.randint(1, 100) <= chance_of_hitting:
            d = self.weapon_wielding.damage
            damage_done = random.randint(int(d/2), d) + self.strength / 10.0
            enemy.take_damage(damage_done)
            self.emit('The %s attacks the %s, doing %s damage!' % (self, enemy, damage_done), ignore=[self, enemy])
            self.perceive('You attack the %s, doing %s damage!' % (enemy, damage_done))
            enemy.perceive('The %s attacks you, doing %s damage!' % (self, damage_done))
            if self not in enemy.enemies:
                enemy.enemies.append(self)
        else:
            self.emit('The %s attacks the %s, but misses.' % (self, enemy), ignore=[self, enemy])
            self.perceive('You attack the %s, but miss.' % (enemy))
            enemy.perceive('The %s attacks you, but misses.' % (self))

    def attack_freq(self):
        try:
            return (20.0/self.dexterity + self.weapon_wielding.unwieldiness + self.armor_worn.unwieldiness)
        except AttributeError:
            return (20.0/self.dexterity)
    
    def die(self, message):
        #What to do when 0 health
        self.emit("The %s dies!" % self, [self])
        corpse = Container("corpse of %s" % (self))
        corpse.add_names("corpse")
        corpse.set_description('corpse of a %s' % (self.short_desc), 'This is a foul-smelling corpse of a %s. It looks nasty.' % (self.short_desc))
        corpse.set_weight(self.weight)
        corpse.set_volume(self.volume)
        corpse.set_max_weight_carried(self.max_weight_carried)
        corpse.set_max_volume_carried(self.max_volume_carried)
        corpse.add_names('corpse')
        self.location.insert(corpse)
        for i in self.contents:
            self.move_to(Thing.ID_dict['nulspace'])      #Moves to a location for deletion. TODO: Make nulspace delete anything inside it.
        self.emit(message)

    def attack_enemy(self, enemy=None):
        """Attack any enemies, if possible, or if a highly aggressive Creature, attack anyone in the room."""
        targets = [x for x in self.location.contents if (isinstance(x, Creature)) and (x != self) and (x.invisible == False)]
        assert self not in targets
        if not targets:
            return
        attacking = enemy
        if not attacking:
            for i in self.enemies:
                if i in self.location.contents and i.invisible == False:
                    attacking = i
                    assert attacking != self
                    break
        if self.aggressive == 2 and not attacking:
            attacking = random.choice(targets)
            self.enemies.append(attacking)
        dbg.debug("Attacking %s" % attacking)
        self.attacking = attacking
        # Figured out who to attack, wield any weapons/armor
        self.weapon_and_armor_grab()

        if self.attack_freq() <= self.attack_now:
            self.attack(attacking)
        else:
            self.attack_now += 1

class NPC(Creature):
    def __init__(self, ID, g, aggressive=0, pref_id=None):
        Creature.__init__(self, ID)
        self.aggressive = aggressive
        self.act_frequency = 3  # how many heartbeats between NPC actions
        self.act_soon = 0       # how many heartbeats till next action
        self.choices = ['move_around', 'talk']  # list of things NPC might do
        if self.aggressive:     # aggressive: 0 = will never attack anyone, even if attacked by them. Will flee. 1 = only attacks enemies. 2 = attacks anyone. highly aggressive.
            self.choices.append('attack_enemy')
        # list of strings that the NPC might say
        self.scripts = []
        self.current_script = None
        self.current_script_idx = 0
        self.attack_now = 0
        self.attacking = False

        g.register_heartbeat(self)
    
    def add_script(self, s):
        self.scripts.append(s)

    def heartbeat(self):
        self.act_soon += 1
        dbg.debug('beat')
        if self.act_soon >= self.act_frequency or (set(self.enemies) & set(self.location.contents)) or self.attacking:
            acting = False
            self.act_soon = 0
            if self.current_script:  # if currently reciting, continue
                self.talk()
                acting = True
            try:
                for i in self.location.contents: # if an enemy is in room, attack
                    if i in self.enemies:
                        if self.aggressive:
                            self.attack_enemy(i)
                        else:  #can't attack (e.g. bluebird)? Run away.
                            self.move_around()
                        acting = True
            except AttributeError:
                dbg.debug('AttributeError, not in any room.')
                return
            if (self.attacking not in self.location.contents) and (self.attacking != False):
                for l in self.location.exits:
                    if l == self.attacking.location:
                        self.move_to(l)
                        moved = True
                        break

#                if not moved:
#                    self.attacking = None
            if not acting:           # otherwise pick a random action
                choice = random.choice(self.choices)
                try:
                    choice_fn = getattr(self, choice)
                    choice_fn()
                except AttributeError:
                    dbg.debug("Object "+self.id+" heartbeat tried to run non-existant action choice "+choice+"!")
            
    def move_around(self):
        """The NPC leaves the room, taking a random exit"""
        try:
            exit_list = list(self.location.exits)
            exit = random.choice(exit_list)
        except (AttributeError, IndexError):
            dbg.debug('no exits, returning')
            return

        dbg.debug("Trying to move to the %s exit!" % (exit))
        current_room = self.location
        new_room = self.location.exits[exit]
        if new_room.monster_safe:
            dbg.debug('Can\'t go to a %s, monster safe room!' % new_room)
            self.move_around()
            return
 
        self.emit("The %s goes %s." % (self, exit))
        self.move_to(new_room)
        self.emit("The %s arrives." % self)
        dbg.debug("Moved to new room %s" % (new_room))
        return

    def talk(self):
        if self.scripts:
            if self.current_script:
                lines = self.current_script.splitlines()
                index = self.current_script_idx
                self.say(lines[index])
                self.current_script_idx += 1
                if self.current_script_idx == len(lines):
                    self.current_script = None
                    self.current_script_idx = 0
            else:
                self.current_script = random.choice(self.scripts)
    