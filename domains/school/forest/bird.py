import creature
import thing

def clone():
    bird = creature.NPC('bird', __file__)
    bird.set_description('bluebird', 'A nice looking little bluebird.')
    bird.set_weight(200)
    bird.set_volume(0.2)
    bird.add_script("""Tweet!""")
    bird.add_script("""Tweet tweet""")
    bird.add_script(
    """Tweet tweet tweet,
    tweet tweet
    tweet, tweet,
    Tweety tweet-tweet""")
    bird.act_frequency = 1

    return bird
