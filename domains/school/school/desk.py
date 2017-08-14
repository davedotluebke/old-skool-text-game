import container
import gametools

def clone():
    desk = container.Container('desk', __file__)
    desk.set_description('carved oak desk', 'This carved oak desk is clearly more than 100 years old, and is carved out in the shapes of dragons and other vicious creatures.')
    desk.fix_in_place('The desk is very, very heavy, and feels rooted to the floor.')
    desk.add_adjectives('carved', 'oak')
    desk.set_prepositions('on', 'onto', 'in', 'into')
    desk.set_max_weight_carried(4e9)
    desk.set_max_volume_carried(80)
    return desk
