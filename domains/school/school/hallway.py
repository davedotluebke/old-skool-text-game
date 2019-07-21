import gametools
import room
import scenery
import thing

class StaffDoorway(scenery.Scenery):
    def __init__(self, default_name, short_desc, long_desc, dest, allowed_players_list='everyone', qkey_number=None):
        super().__init__(default_name, short_desc, long_desc)
        self.dest = gametools.load_room(dest)
        self.allowed_players_list = allowed_players_list
        self.actions.append(scenery.Action(self.enter_door, ['open', 'enter'], True, False))
        self.add_response(['kick', 'hit', 'punch', 'chop'], 'The door is firmly closed, and you only manage to gain a bruise.')
        self.actions.append(scenery.Action(self.open, ['insert', 'put'], True, False))
        self.unlisted = True
        self.keyq = qkey_number
        self.locked = True
        
    def enter_door(self, p, cons, oDO, oIDO):
        if self.keyq != None and self.locked:
            cons.user.perceive('The door is locked.')
            return True
        if (self.keyq != None and not self.locked) or self.allowed_players_list == 'everyone' or cons.user.names[0] in self.allowed_players_list:
            try:
                cons.user.move_to(self.dest)
                cons.user.perceive('You open the door and step through.')
                self.dest.report_arrival(cons.user)
                return True
            except:
                return "For some reason you can't go through the door."
        else:
            cons.user.perceive('The door is locked.')
            return True
    
    def open(self, p, cons, oDO, oIDO):
        if hasattr(oDO, 'qkey_number') and oDO.qkey_number == self.keyq:
            cons.user.perceive('You unlock the door.')
            self.locked = False
            oDO.move_to(thing.Thing.ID_dict['nulspace'])
            return True
        else:
            cons.user.perceive("You try to put the %s in the keyhole, but it doesn't fit." % oDO.names[0])
            return True

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    hallway = room.Room('hallway', roomPath, safe=True, indoor=True)
    hallway.indoor = True
    hallway.set_description('staff office hallway', 'This hallway leads to all of the staff offices. '
    'It is very blank on the walls, however the walls themselves are intricate and have little carved patterns in them. '
    'Six doors lead off of this hallway, each decorated with a metal carving of a different animal:'
    'a serpent, a parrot, a dragon, a goblin, a dolphin, and a dragonfly.')
    hallway.add_adjectives('staff', 'office')
    hallway.add_exit('south', 'domains.school.school.gallery')

    serpents_door = StaffDoorway('door', 'door with a carving of a serpent on it', 
    'This is a strong oak door with a bronze carving of a serpent on it.', 'domains.school.school.empty_office')
    serpents_door.add_adjectives('serpent', 'serpents', 'serpent\'s', 'oak', 'bronze')
    hallway.insert(serpents_door, True)

    parrots_door = StaffDoorway('door', 'door with a carving of a parrot on it', 
    'This is a strong cherry wood door with a silver carving of parrot on it.', 'home.fastar.entryway', ['fastar', 'scott', 'tate', 'john', 'odshinstar', 'fredd', 'cedric'])
    parrots_door.add_adjectives('parrot', 'parrots', 'parrot\'s', 'beutiful', 'cherry', 'silver')
    hallway.insert(parrots_door, True)

    dragons_door = StaffDoorway('door', 'door with a carving of a dragon on it',
    'This is a strong maple door with a gold carving of a dragon on it.', 'domains.centrata.firefile_area.key_quest.spring_room', qkey_number=3)
    dragons_door.add_adjectives('dragon', 'dragons', 'dragon\'s', 'maple', 'gold')
    hallway.insert(dragons_door, True)

    goblins_door = StaffDoorway('door', 'door with a carving of a goblin on it',
    'This is a weak pine door with a lead carving of a goblin on it.', 'domains.school.school.empty_office')
    goblins_door.add_adjectives('goblin', 'goblins', 'goblin\'s', 'lead', 'pine')
    hallway.insert(goblins_door, True)

    dragonflys_door = StaffDoorway('door', 'door with a carving of a dragonfly on it',
    'This is a strong birch door with a copper carving of a dragonfly on it.', 'home.scott.house.lr31795', ['scott', 'fastar', 'tate', 'john', 'cedric'])
    dragonflys_door.add_adjectives('dragonfly', 'dragonflys', 'dragonfly\'s', 'copper', 'birch')
    hallway.insert(dragonflys_door, True)

    dolphins_door = StaffDoorway('door', 'door with a carving of a dolphin on it',
    'This is a strong teak wood door with a brass carving of a dolphin on it.', 'home.cedric.blank_room', ['cedric','scott','fastar','tate'])
    dolphins_door.add_adjectives('dolphin', 'dolphins', 'dolphin\'s', 'teak', 'brass', 'wood')
    hallway.insert(dolphins_door, True)

    otters_door = StaffDoorway('door','door with a carving of two otters on it',
    'THis is a strong palm wood door with a platnum carving of two sea otters playing on it.', 'home.tate.entry', ['tate', 'scott', 'fastar', 'cedric'])
    otters_door.add_adjectives('otter', 'otters', 'otter\'s', 'platnum', 'palm')
    hallway.insert(otters_door, True)

    return hallway
