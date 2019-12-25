import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    blacksmith_shop = room.Room('blacksmith', roomPath)
    blacksmith_shop.set_description("blacksmith's shop", 
        "You are in a low, dark room lit by a few small windows and the occasional bright orange glow "
        "of coals when the smith works the bellows. Many examples of the blacksmith's art adorn the "
        "walls and hang from the ceilings, from horseshoes to nails to various tools and farm implements. "
        "To your west you can exit to the street. ")
    blacksmith_shop.add_exit('west', 'domains.centrata.firefile_area.village.south_village')

    horseshoes = scenery.Scenery('horseshoes', 'horseshoes', 'Several horseshoes of all sizes are nailed to the '
        'wall, all facing upwards for good luck. ', unlisted=True)
    horseshoes.add_names('horseshoe')
    horseshoes.add_response(['take', 'get', 'pry', 'remove'], 'The horseshoes are nailed to the wall.')
    horseshoes.move_to(blacksmith_shop, True)

    bellows = scenery.Scenery('bellows', 'coal-fired bellows', "This bellows apparatus "
        "pumps air over the coals when the blacksmith turns a crank, causing them to glow brightly "
        "with a white-hot heat.", unlisted=True)
    bellows.add_adjectives('coal-fired')
    
    anvil = scenery.Scenery('anvil', 'iron anvil', "This essential tool of the smith's "
        "trade is used for pounding and shaping the red-hot iron taken from the forge.", unlisted=True, )
    anvil.add_adjectives('iron')

    tools = scenery.Scenery('tools', 'tools and farm implements', "The blacksmith has "
        "hung several tools and farm implements around the shop, though you aren't sure of the "
        "purpose of any of them.", unlisted=True)
    tools.add_names('nails', 'nail', 'tool', 'implements')
    tools.add_adjectives('farm', 'various')

    bellows.move_to(blacksmith_shop, True)
    anvil.move_to(blacksmith_shop, True)
    tools.move_to(blacksmith_shop, True)

    smith = gametools.clone('domains.centrata.firefile_area.village.blacksmith')
    smith.move_to(blacksmith_shop)
    return blacksmith_shop