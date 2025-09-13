import shop
import gametools
import player

class Innkeeper(shop.Shopkeeper):
    def __init__(self):
        super().__init__('barnabas', __file__, None)
        self.orc_quest_completed = False

    def heartbeat(self):
        if not self.orc_quest_completed:
            for i in self.location.contents:
                if isinstance(i, player.Player):
                    for j in i.contents:
                        if hasattr(j, 'orc_quest') and j.orc_quest:

                            # offer the reward if they haven't already completed the quest
                            if not i.test_quest("Bring the orc chief's helmet to the innkeeper"):
                                self.orc_quest_completed = True
                                self.say("""Congratulations again on your victory! The whole village is grateful to you.""")
                                self.say("""Here's your reward, adventurer.  I'm sure you'll find a use for it.""")
                                reward = gametools.clone('domains.centrata.village.gold_piece')
                                reward.plurality = 10
                                reward.move_to(i)
                                i.complete_quest("Bring the orc chief's helmet to the innkeeper")
                                j.orc_quest = False  # this helmet object has now been used to satisfy the quest
                                # add the new quest-completed scripts
                                self.scripts = []
                                self.add_script("""Now the orcs are taken care of, the village will prosper.""")
                                self.add_script("""Our tourist industry is sure to take off. Tourists like prairies, right?""")
                                break
                    else:
                        if not i.test_quest("Bring the orc chief's helmet to the innkeeper"):
                            i.add_quest("Bring the orc chief's helmet to the innkeeper")

        return super().heartbeat()

def clone():
    innkeeper = Innkeeper('barnabas', __file__, None)
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
