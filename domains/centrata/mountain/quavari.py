import creature
import gametools

def clone():
    quavari = creature.NPC('quavari', __file__, aggressive=1, movement=0)
    quavari.set_description('quavari', 'A large, black bird with red stripes under its wings, the Quavari appears intimidating when inspected.')
    quavari.set_weight(1000)
    quavari.set_volume(1)
    quavari.set_combat_vars(35, 40, 30, 60) # adjust these to make the encounter more exciting
    quavari.act_frequency = 1

    beak = gametools.clone('domains.centrata.mountain.quavari_beak')
    quavari.set_default_weapon(beak)

    claws = gametools.clone('domains.centrata.mountain.quavari_claws')
    quavari.set_default_weapon(claws, True)

    quavari.weapon_wielding = None # XXX this shouldn't be a necessary patch

    return quavari
