import thing
import gametools

def clone():
    pen = thing.Thing('pen', __file__)
    pen.set_description('balpoint pen', 'This is a fancy black ball point pen, sadley it apears to be out of ink.')
    pen.set_weight(3)
    pen.set_volume(0.001)
    pen.add_adjectives('fancy', 'ballpoint', 'ball-point', 'ball point', 'empty', 'black')

    return pen