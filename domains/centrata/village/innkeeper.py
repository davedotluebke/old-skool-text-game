import shop
import gametools

def clone():
    innkeeper = shop.Shopkeeper('innkeeper', __file__, None)
    innkeeper.set_description('cheerful innkeeper', 'Behind the bar stands the innkeeper, a rotund, bewhiskered "
        'human with a cheerful face and shrewd eyes.')
    innkeeper.set_welcome_message('Greetings, my good &s&u!  I am Barnabas, keeper of this bar and sometime mayor '
        'of the village. Welcome to my humble inn.  What can I get you?')
    innkeeper.set_auto_introduce(True)
    innkeeper.add_adjectives('cheerful', 'shrewd', 'bewhiskered', 'whiskered', 'rotund')

    innkeeper.act_frequency = 7
    innkeeper.set_default_items(gametools.clone('domains.centrata.village.hook'))
    innkeeper.add_act_script("""The blacksmith pumps the bellows, and the coals glow white-hot.""")
    innkeeper.add_act_script("""The blacksmith hammers a piece of iron on the anvil.""")
    innkeeper.add_act_script("""The blacksmith dunks a piece of iron in water to cool it down, causing steam to fly up.""")
    innkeeper.add_act_script("""The blacksmith hammers a piece of iron into a hook shape.""")
    innkeeper.add_script("""The orc raiding parties have been getting worse as of late.
    Decent people can't go out their own doors at night.""")
    innkeeper.add_script("""I heard the orcs are camped somewhere out to the east.""")
    innkeeper.add_script("""We could probably fight off those dang orcs ourselves if it wasn't for their big chief.
    The mayor's offering a reward of ten gold pieces to whoever brings back proof that he's dead.""")
    innkeeper.add_script("""I'm making this piece for our mayor - that's the innkeeper, you know. His carriage needs fixin.""")

    return innkeeper
