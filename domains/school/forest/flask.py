import container
import liquid

def clone():
    flask = container.Container('flask', __file__)
    flask.set_description('small flask', 'This is a small flask of clear glass. ')
    flask.add_adjectives('small', 'clear', 'glass')
    flask.set_max_volume_carried(0.050)
    flask.set_max_weight_carried(200)
    flask.liquid = True

    molasses = liquid.Liquid('molasses')
    molasses.set_description('thick brown molasses', 'This brownish liquid is sweet and thick. Not surprisingly, it is used in recipes as a sweetener and a thickener.')
    molasses.add_adjectives('thick', 'brown', 'brown', 'brownish')
    molasses.set_volume(0.040)
    molasses.set_weight(40)

    flask.insert(molasses)

    return flask
