import container
import gametools
import action

def clone():
    kleenex_box = container.Container("box", __file__)
    kleenex_box.set_description("kleenex box", "This kleenex box is a bright blue. It looks almost brand new. ")
    kleenex_box.add_adjectives("blue", "new")
    kleenex_box.set_max_weight_carried(100)
    kleenex_box.set_max_volume_carried(0.5)
    kleenex_box.set_weight(0.01)
    kleenex_box.set_volume(0.5)

    for i in range(0, 50):
        tissue = gametools.clone("domains.renaissance_school.tissue")
        tissue.move_to(kleenex_box, True)

    return kleenex_box
