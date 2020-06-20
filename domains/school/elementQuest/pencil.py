import thing
import gametools

def clone():
    pencil = thing.Thing('pencil', __file__)
    pencil.set_flammable(2)
    pencil.set_description('dull pencil', 'This is a black wooden charcoal pencile. It is dull.')
    pencil.add_adjectives('charcoal', 'dull', 'wooden', 'black')
    pencil.burn_time = 11
    pencil.set_volume(0.0005)
    pencil.set_weight(7)

    return pencil