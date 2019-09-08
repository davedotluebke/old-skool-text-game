import container

# XXX unfinished - needs capacity weight volume etc
def clone():
    glass_bottle = container.Container('bottle', __file__)
    glass_bottle.set_description("normal glass bottle","This is a normal glass bottle. It looks quite usable.")
    glass_bottle.liquid = True

    return glass_bottle

