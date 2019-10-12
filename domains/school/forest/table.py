import gametools
import container

def clone():
    table = container.Container('table', __file__)
    table.set_description("kitchen table", "This dated-looking kitchen table has chrome edging and a Formica top.")
    table.fix_in_place("The table is too heavy and awkward to move.")
    table.add_adjectives("kitchen", "dated", "formica")
    table.set_prepositions("on", "onto")
    table.set_max_volume_carried(5000)
    table.set_max_weight_carried(150000)

    bottle = gametools.clone('domains.school.forest.bottle')
    table.insert(bottle)

    plate = gametools.clone('domains.school.forest.plate')
    table.insert(plate)
    return table
