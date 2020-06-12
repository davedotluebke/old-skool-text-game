import thing

def clone():
    price_tag_bundle = thing.Thing('bundle', __file__)
    price_tag_bundle.set_description('price tag bundle', 'This is a bundle of blank pirce tags, you wounder what they are for.')
    price_tag_bundle.add_adjectives('price', 'tag', 'bundle')
    price_tag_bundle.add_names('tags')
    price_tag_bundle.set_weight(13)
    price_tag_bundle.set_volume(0.0001)

    return price_tag_bundle