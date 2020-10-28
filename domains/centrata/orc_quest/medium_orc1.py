import creature
import gametools
import thing

class Orc(creature.NPC):
    def is_forbidden(self, r):
        # Check whether the creature is allowed to enter room `r`.
        # `r` is string containing the path to the room
        # return True if the room is forbidden
        return False

def clone():
    orc = Orc('orc', __file__, aggressive=2)
    orc = creature.NPC('orc', __file__, aggressive=2)
    orc.set_description('burly orc', "This burly orc looks muscular and threatening.")
    orc.add_adjectives('burly', 'muscular', 'threatening')
    orc.set_combat_vars(35, 50, 60, 40)
    orc.act_frequency = 2
   
    sword = gametools.clone("domains.centrata.orc_quest.orc_sword")
    sword.move_to(orc)

    hide = gametools.clone("domains.centrata.orc_quest.orc_hide")
    hide.move_to(orc)

    return orc