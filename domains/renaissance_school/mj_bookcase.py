import container
import gametools

def clone():
    bookcase = container.Container("bookcase", __file__)
    bookcase.set_description("bookcase", "This bookcase is made of lighly stained wood. It is partially blocking the door.", unlisted=True)
    bookcase.add_adjectives("lightly", "stained", "light")
    bookcase.set_prepositions('on', 'onto', 'in', 'into')
    bookcase.fix_in_place("This desk is to heavy and awkward to move.")
    bookcase.set_max_weight_carried(4e9)
    bookcase.set_max_volume_carried(3e9)

    # TODO: put books onto the shelf

    return bookcase
