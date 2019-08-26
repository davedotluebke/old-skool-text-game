import shop
import gametools

def clone():
    shopkeeper = shop.Shopkeeper('shopkeeper', __file__, None)
    shopkeeper.set_description('ordinary shopkeeper', 'This shopkeeper owns the shop you are standing in now.')
    shopkeeper.set_default_items(gametools.clone('domains.school.forest.sword'), gametools.clone('domains.school.forest.leather_suit'))
    shopkeeper.add_items(gametools.clone('domains.school.school.dragon_scale'))
    return shopkeeper
