import container

def clone():
    flask = container.Container('flask', __file__)
    flask.set_description('clear flask', 'This is a clear glass flask. It is slightly warm to the touch.')
    flask.add_adjectives('warm', 'clear', 'glass')
    flask.liquid = True
    return flask