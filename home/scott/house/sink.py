import home.scott.house.faucetThings as faucetThings

def clone():
    sink = faucetThings.FaucetThing('sink', __file__, 'porcelin sink', 'This is a ordinary bathroom sink made of porcelin. It has a clean metal faucet.', 'sink')
    sink.add_adjectives('porcelin', 'metal', 'clean', 'modern')
    return sink
