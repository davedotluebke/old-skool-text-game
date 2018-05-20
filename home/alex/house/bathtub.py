import home.alex.house.faucetThings as faucetThings

def clone():
    bathtub = faucetThings.FaucetThing('bathtub', __file__, 'white bathtub', 'This bathtub is white. It has a faucet on one end of the tub and a shower above.', 'bathtub')
    bathtub.add_adjectives('modern', 'white')
    return bathtub
