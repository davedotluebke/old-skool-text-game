import thing

def clone():
    flower_pot = thing.Thing('pot', __file__)
    flower_pot.set_description('flower pot', 'This large flower is pot packed full of beutiful roses.', unlisted=True)
    flower_pot.add_adjectives('rose', 'flower', 'large', 'packed')
    flower_pot.set_weight(3175)
    flower_pot.set_volume(6)

    return flower_pot