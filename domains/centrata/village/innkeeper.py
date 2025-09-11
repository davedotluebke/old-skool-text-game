import shop
import gametools

def clone():
    innkeeper = shop.Shopkeeper('barnabas', __file__, None)
    innkeeper.add_names('innkeeper')
    innkeeper.set_description('cheerful innkeeper', 'Behind the bar stands the innkeeper, a rotund, bewhiskered '
        'human with a cheerful face and shrewd eyes.')
    innkeeper.set_welcome_message('Greetings, my good &s&u!  I am Barnabas, keeper of this bar and sometime mayor '
        'of the village. Welcome to my humble inn.  What can I get you?')
    innkeeper.set_auto_introduce(True)
    innkeeper.add_adjectives('cheerful', 'shrewd', 'bewhiskered', 'whiskered', 'rotund')

    innkeeper.act_frequency = 7
    innkeeper.set_default_items(gametools.clone('domains.centrata.village.hook'))
    innkeeper.add_act_script("""The innkeeper pours a glass of ale.""")
    innkeeper.add_act_script("""The innkeeper polishes the bar.""")
    innkeeper.add_script("""You're a newcomer to our town, I see.  Adventurer, by the look of you.""")
    innkeeper.add_script("""We have a wee orc problem.  I'll give a prize to anyone who brings me proof the orc chief is dead.""")
    innkeeper.add_script("""Not saying it won't be dangerous -- some of the orcs are pushovers, but their chief is a different story.""")
    innkeeper.add_script("""Ten gold pieces, that's my prize.  Show me the helmet of the orc chief, and I'll give you the gold.""")

    return innkeeper
