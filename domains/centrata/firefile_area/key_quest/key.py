import thing

def clone():
    key = thing.Thing('key', __file__)
    key.set_description('old brass key', 'This is an old key made of brass.')
    key.add_adjectives('old', 'brass')
    key.qkey_number = 0
    return key