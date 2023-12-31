import container

def clone():
    bucket = container.Container('bucket', __file__)
    bucket.set_description('steel bucket', 'This bucket is made of a thick steel. It is quite heavy.')
    bucket.liquid = True
    bucket.add_adjectives('steel', 'thick')
    return bucket
