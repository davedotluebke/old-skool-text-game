import gametools
import container 

def clone():
    b_table = container.Container('table', __file__)
    b_table.set_description('banquet-size table', 'This is a extremely long banquet table, '
        'stretching almost from one end of the room to the other.', unlisted=True)
    b_table.fix_in_place('Moving this table would require a lot of help.')
    b_table.add_adjectives('massive', 'enormous', 'long', 'banquet')
    b_table.set_prepositions('on', "onto")
    b_table.set_max_weight_carried(4e9)
    b_table.set_max_volume_carried(3e9)
    return b_table
