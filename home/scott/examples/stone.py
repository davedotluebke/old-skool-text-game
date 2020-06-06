import stones

def clone():
    stone = stones.Stone('stone', __file__, 100, 100)
    stone.set_description('ordinary stone', 'This is an ordinary stone, created for testing purposes.')
    stone.add_adjectives('ordinary')
    return stone
