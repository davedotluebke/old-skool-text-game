import container
import gametools

def clone():
    wardrobe = container.Container('wardrobe', __file__)
    wardrobe.set_description('large wardrobe', 'This large wardrobe stands against one wall.', unlisted=True)
    wardrobe.add_adjectives('large')
    wardrobe.fix_in_place('The wardrobe is too large and heavy to move.')

    hanger = gametools.clone('domains.school.elementQuest.clothes_hanger')
    hanger.plurality = 10
    wardrobe.insert(hanger)

    wardrobe.closable = True
    wardrobe.close()
    return wardrobe
