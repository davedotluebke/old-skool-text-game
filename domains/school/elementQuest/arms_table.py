import container

def clone():
    arms_table = container.Container('table', __file__)
    arms_table.set_description('table with coat of arms', 'This is a large stone table in the middle of the room. '
    'Carved into the table is a large coat of arms, with two swallows holding up a banner with four flying swallows '
    'pictured on it.', unlisted=True)
    arms_table.add_adjectives('arms', 'coat', 'swallow')
    arms_table.set_prepositions('on', 'onto')
    arms_table.fix_in_place('The stone table is too heavy to move.')
    arms_table.set_max_volume_carried(4000)
    arms_table.set_max_weight_carried(4e9)
    return arms_table
