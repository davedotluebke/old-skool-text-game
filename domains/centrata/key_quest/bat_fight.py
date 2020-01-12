import gametools
import scenery
import room
import domains.centrata.key_quest.keyholemod as k

class BatFightRoom(room.Room):
    def go_to(self, p, cons, oDO, oIDO):
        if p.words[1] == 'south':
            if cons.user not in self.keyhole.checked_players:
                return "I'm not sure how to go south!"
        return super().go_to(p, cons, oDO, oIDO)

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = BatFightRoom('cave', roomPath, indoor=True)
    r.set_description('cave', '''You find yourself in a large cave with a mostly flat floor. 
    Stalagtites cover the ceiling, and many matching stalagmites cover the floor. Strangely,
    there seems to be no water here, except a few drips that fall from the ceiling. The only
    obvious opening is a small gap in the ceiling at the north end of the room. There almost 
    seems to be a keyhole in the south wall, but you can't be sure''')

    stalagtite = scenery.Scenery('stalagtite', 'large stalagtite', 'This is a particularly large stalagtite that hangs off of the ceiling.')
    stalagtite.add_response(['climb'], 'Unfortunately, you can\'t mannage to get a hold of the stalagtite, because it is too high.')
    r.insert(stalagtite, True)

    bat = gametools.clone('domains.centrata.key_quest.bat')
    bat.have_key()
    r.insert(bat, True)

    keyhole = k.Keyhole('south', 'domains.centrata.key_quest.maze_entrance', 1)
    r.insert(keyhole, True)
    r.keyhole = keyhole

    return r