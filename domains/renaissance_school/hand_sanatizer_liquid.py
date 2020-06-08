import liquid

def clone():
    sanatizer = liquid.Liquid('sanatizer', __file__)
    sanatizer.set_description('hand sanatizer', 'This alcohol-based hand sanitizer can be used to clean your hands.')
    sanatizer.add_adjectives('hand', 'alcohol')
    sanatizer.set_volume(0.3)
    sanatizer.set_weight(100)
    return sanatizer
