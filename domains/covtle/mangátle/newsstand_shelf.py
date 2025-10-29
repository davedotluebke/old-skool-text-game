import container
import gametools

def clone():
    shelf = container.Container('shelf', __file__)
    shelf.set_description('pine wood shelf', 'This pine wood shelf is fastened to the stone wall, and is filled with newspapers, magazines, and books for sale.')
    shelf.add_adjectives('pine', 'wood')

    lelvlai_ad_mangátle = gametools.clone('domains.covtle.mangátle.lelvlai_ad_mangátle')
    lelvlai_ad_mangátle.plurality = 50
    lelvlai_ad_mangátle.move_to(shelf, True)

    return shelf
