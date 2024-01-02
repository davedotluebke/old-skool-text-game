import container
import gametools

def clone():
    shelf = container.Container('shelf', __file__)
    shelf.set_description('white shelf', 'This white-painted shelf is built into the wall.')
    shelf.closable = False
    shelf.add_adjectives('white')
    shelf.set_prepositions('on', 'onto')
    
    return shelf
