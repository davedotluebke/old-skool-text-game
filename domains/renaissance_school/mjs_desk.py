import container
import gametools

def clone():
    desk = container.Container("desk", __file__)
    desk.set_description("large black desk", "This large desk appears to be made from a black plastic. It has several sections, "
    "some of which are higher than others.", unlisted=True)
    desk.add_adjectives("large", "black", "multilevel")
    desk.set_prepositions('on', 'onto')
    desk.fix_in_place("This desk is to heavy and awkward to move.")
    desk.set_max_weight_carried(4e9)
    desk.set_max_volume_carried(80)
    return desk
