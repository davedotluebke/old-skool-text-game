import gametools
import thing
from domains.centrata.orc_quest.orc import Orc

def clone():
    orc = Orc('orc', __file__, aggressive=2)
    orc.set_orc_range(2)
    orc = Orc('orc', __file__, aggressive=2)
    orc.set_description('burly orc', "This burly orc looks muscular and threatening.")
    orc.add_adjectives('burly', 'muscular', 'threatening')
    orc.set_combat_vars(35, 50, 60, 40)
    orc.act_frequency = 2

    sword = gametools.clone("domains.centrata.orc_quest.orc_sword")
    sword.move_to(orc)

    hide = gametools.clone("domains.centrata.orc_quest.orc_hide")
    hide.move_to(orc)

    return orc