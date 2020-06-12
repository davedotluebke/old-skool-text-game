import container
import gametools

def clone():
    changing_table = container.Container('table', __file__)
    changing_table.set_description('changing table','This is a simple and plain changing table. On it you see a tisue box.', unlisted=True)
    changing_table.set_max_volume_carried(12)
    changing_table.set_max_weight_carried(90000)
    changing_table.add_adjectives('changing', 'simple', 'plain')
    changing_table.add_names('place', 'changer')
    changing_table.fix_in_place('The table is suprisingly heavy.')

    tisue_box = gametools.clone('domains.renaissance_school.kleenex')
    changing_table.insert(tisue_box)

    hand_sanitiser = gametools.clone('domains.renaissance_school.hand_sanitiser')
    changing_table.insert(hand_sanitiser)

    return changing_table