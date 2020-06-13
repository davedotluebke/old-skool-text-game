import thing
import gametools

def clone():
    paper = thing.Thing('paper', __file__)
    paper.add_adjectives('sheet', 'of', 'blank', 'white')
    paper.set_volume(0.00001)
    paper.set_weight(4.5)
    paper.set_description('blank sheet of paper', 'This is a blank sheet of white printer paper.')
    paper.set_flammable(8)
    paper.add_names('sheet')
    paper.burn_time = 3

    return paper