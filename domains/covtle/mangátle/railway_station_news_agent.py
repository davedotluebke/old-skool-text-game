import shop
import gametools

def clone():
    news_agent = shop.Shopkeeper('news agent', __file__, None)
    news_agent.set_description('young news agent', 'This young news agent is smiling as she watches over the shop.')
    news_agent.set_welcome_message('Hi! Welcome to Mangátle!')
    news_agent.add_adjectives('smiling', 'young')
    news_agent.act_frequency = 5
    news_agent.set_default_items(gametools.clone('domains.covtle.mangátle.lelvlai_ad_mangátle'))
    news_agent.add_act_script("""The news agent sorts through some papers behind her desk.""")
    news_agent.add_script("""It's always so fun when new students come to town!""")
    news_agent.add_script("""Let me know if you'd like to buy anything! I have a copy of Lelvlai ad Mangátle!""")
    news_agent.add_script("""If you're looking for the university, you need to take the orange tram. The purple won't get you there!""")

    return news_agent
