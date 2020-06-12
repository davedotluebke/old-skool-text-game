import gametools
import container

def clone():
    desk = container.Container('desk', __file__)
    desk.set_max_weight_carried(30000)
    desk.set_max_volume_carried(90)
    desk.set_description('sturdy desk', 'This is a sturdy desk made of dark oak behind it ther is a chair. It and everything on it is coated in a thin layer of dust, as if it hasn\'t been used in years.')
    desk.add_adjectives('sturdy', 'dark', 'oak')
    desk.add_names('table')

    prism = gametools.clone('domains.school.elementQuest.')