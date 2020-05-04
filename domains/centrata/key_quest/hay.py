import thing

def clone():
    hay = thing.Thing("hay", __file__)
    hay.set_description("pice of hay", "This is a normal piece of hay.")
    hay.add_adjectives("normal")

    return hay

