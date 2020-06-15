import container

def clone():
    bedside_table = container.Container('table', __file__)
    bedside_table.set_description('bedside table', 'This is a small bedside table, with two levels of shelving.', unlisted=True)
    bedside_table.add_adjectives('bedside', 'small')
    bedside_table.set_prepositions('on', 'onto')
    bedside_table.set_max_volume_carried(30)
    bedside_table.set_max_weight_carried(19987)
    return bedside_table
