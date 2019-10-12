import liquid

def clone():
    molasses = liquid.Liquid('molasses', __file__)
    molasses.set_description('thick brown molasses', 'This brownish liquid is sweet and thick. Not surprisingly, it is used in recipes as a sweetener and a thickener.')
    molasses.add_adjectives('thick', 'brown', 'brownish')
    molasses.set_volume(0.040)
    molasses.set_weight(40)
    return molasses
