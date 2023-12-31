import container
import gametools

def clone():
    bushes = container.Container('bush', __file__)
    bushes.set_description('immaculately trimmed hedge', 'This immaculately trimmed hedge stands on both sides of the gate.', unlisted=True)
    bushes.add_adjectives('immaculately', 'trimmed')
    bushes.add_names('hedge')

    key = gametools.clone('domains.centrata.mansion.gate_key')
    bushes.insert(key, True)
    
    return bushes
