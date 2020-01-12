import creature
import gametools
import thing

def clone():
    orc = creature.NPC('orc', __file__, aggressive=2)
    orc.set_description('scrawny orc', "This scrawny orc is disgusting but not particularly fearsome.  "
        "It is unarmed and unarmored, except for its fists and tough leathery skin.  It looks clumsy but mean.")
    orc.add_adjectives('scrawny', 'disgusting')
    orc.set_combat_vars(30, 40, 50, 40)
    orc.act_frequency = 2
    return orc