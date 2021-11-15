import thing
import gametools

def clone():
    example = thing.Thing('example', __file__)
    example.set_description('example object', 'This is a new (Nov 14, 2021) example object for testing purposes.')
    example.add_adjectives('example', 'notional')
    return example
