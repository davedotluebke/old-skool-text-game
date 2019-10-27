import container
import liquid
import gametools

def clone():
    flask = container.Container('flask', __file__)
    flask.set_description('small flask', 'This is a small flask made of clear glass. ')
    flask.add_adjectives('small', 'clear', 'glass')
    flask.set_max_volume_carried(0.050)
    flask.set_max_weight_carried(200)
    flask.liquid = True

    molasses = gametools.clone('domains.school.forest.molasses')
    flask.insert(molasses)

    return flask
