import container
import gametools

def clone():
    shelf = container.Container('shelf', __file__)
    shelf.set_description('white shelf', 'This white-painted shelf is built into the wall.', unlisted=True)
    shelf.closable = False
    shelf.add_adjectives('white')
    shelf.set_prepositions('on', 'onto')

    teddy_bears = gametools.clone('domains.centrata.mansion.teddy_bear')
    teddy_bears.plurality = 5
    shelf.insert(teddy_bears, True)

    return shelf
