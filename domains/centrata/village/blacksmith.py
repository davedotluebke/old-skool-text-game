import shop
import gametools

def clone():
    smith = shop.Shopkeeper('blacksmith', __file__, None)
    smith.set_description('grizzled blacksmith', 'This grizzled old blacksmith looks as if he has worked '
        'behind this forge for a hundred years.')
    smith.set_welcome_message('Welcome to my smithy, my good &s&u!')
    smith.add_adjectives('grizzled', 'old')
    smith.act_frequency = 7
    smith.set_default_items(gametools.clone('domains.centrata.village.hook'))
    smith.add_act_script("""The blacksmith pumps the bellows, and the coals glow white-hot.""")
    smith.add_act_script("""The blacksmith hammers a piece of iron on the anvil.""")
    smith.add_act_script("""The blacksmith dunks a piece of iron in water to cool it down, causing steam to fly up.""")
    smith.add_act_script("""The blacksmith hammers a piece of iron into a hook shape.""")
    smith.add_script("""The orc raiding parties have been getting worse as of late.
    Decent people can't go out their own doors at night.""")
    smith.add_script("""I heard the orcs are camped somewhere out to the east.""")
    smith.add_script("""We could probably fight off those dang orcs ourselves if it wasn't for their big chief.
    The mayor's offering a reward of ten gold pieces to whoever brings back proof that he's dead.""")
    smith.add_script("""I'm making this piece for our mayor - that's the innkeeper, you know. His carriage needs fixin.""")

    return smith
