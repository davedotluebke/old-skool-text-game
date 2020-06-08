import thing
import domains.centrata.key_quest.scrollmod as scrollmod

def clone():
    scroll1 = scrollmod.Scroll('scroll', __file__, 'new scroll', 
    'This scroll is a new scroll. The ink seems as if it might still be wet.',
    '''Find thyself a dragon's door
    To find thyself a spring
    Then take thyself a dragon's scale
    And get thyself some hay to bail
    A poppy's seed thou must not bring
    To a secret shack upon the moor
    ''')
    scroll1.add_adjectives('new')
    return scroll1
