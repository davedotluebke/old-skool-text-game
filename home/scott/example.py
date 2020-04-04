import thing
import gametools

def clone():
    example = thing.Thing('example', __file__)
    example.set_description('example object', 'This is an example object for testing purposes.')
    return example
