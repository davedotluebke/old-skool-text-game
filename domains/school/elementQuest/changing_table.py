import container
import gametools

def clone():
    changing_table = container.Container('table', __file__)
    changing_table.set_description('This is a simple and plain changing table. On it you see a tisue box.', unlisted=True)
    changing_table.set_max_volume_carried(12)
    changing_table.set_max_weight_carried(90000)
    changing_table.add_adjectives('changing', 'simple', 'plain')
    changing_table.add_names('place', 'changer')

    tisue_box = gametools.clone('domains.renaissance_school.kleenex_box')
    changing_table.insert(tisue_box)

    return changing_table