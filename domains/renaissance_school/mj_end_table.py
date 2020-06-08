import container
import gametools

def clone():
    end_table = container.Container("table", __file__)
    end_table.set_description("end table", "This small black end table appears to match the desk.", unlisted=True)
    end_table.add_adjectives("end")
    end_table.set_prepositions('on', 'onto')
    end_table.set_max_weight_carried(4e9)
    end_table.set_max_volume_carried(3e9) # XXX real weight and volume checks, end table should not be a bag of holding

    hand_sanatizer = gametools.clone("domains.renaissance_school.hand_sanatizer")
    hand_sanatizer.move_to(end_table, True)

    kleenex_box = gametools.clone("domains.renaissance_school.kleenex_box")
    kleenex_box.move_to(end_table, True)

    return end_table
