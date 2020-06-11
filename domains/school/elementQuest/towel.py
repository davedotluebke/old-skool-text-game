import gametools
import thing

def clone():
    towel = thing.Thing('towel', 'beach towel', 'This is a large blue beach towel. It does not currently have any sand on it.')
    towel.add_adjectives('blue', 'beach', 'large')
    towel.set_weight(750)
    towel.set_volume(5)