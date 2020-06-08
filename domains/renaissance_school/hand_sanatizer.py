import container
import gametools
import action

class HandSanitizerDispenser(container.Container):
    def use_dispenser(self, p, cons, oDO, oIDO):
        cons.user.perceive("You squirt some hand sanatizer into your hands and use it.")
        return True
    
    actions = dict(container.Container.actions)
    actions['use'] = action.Action(use_dispenser, True, False)
    actions['squirt'] = action.Action(use_dispenser, True, False)

def clone():
    dispenser = HandSanitizerDispenser("dispenser", __file__)
    dispenser.set_description("hand sanitizer dispenser", "This hand sanatizer dispenser has a green label, "
    "and is filled with green-coloured hand sanatizer. It almost seems as if it is brand-new. ", unlisted=True)
    dispenser.liquid = True
    dispenser.add_adjectives("hand", "sanatizer", "new")
    dispenser.add_names("sanatizer", "bottle")
    dispenser.set_max_weight_carried(1000)
    dispenser.set_max_volume_carried(0.3)
    dispenser.set_weight(1000)
    dispenser.set_volume(0.3)

    sanatizer_liquid = gametools.clone("domains.renaissance_school.hand_sanatizer_liquid")
    sanatizer_liquid.move_to(dispenser, True)

    return dispenser
