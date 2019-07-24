import domains.school.flower as flowerMod
import action

def clone():
    poppy = flowerMod.Flower("poppy", __file__, 'poppy')
    poppy.set_description("red poppy","This poppy is VERY pretty! You really want to pick it!")
    poppy.set_volume(2.122)
    poppy.set_weight(200)
    poppy.add_adjectives("very","pretty")
    poppy.actions = dict(flowerMod.Flower.actions)
    poppy.actions['pick'] = action.Action(flowerMod.Flower.take, True, False)
    return poppy