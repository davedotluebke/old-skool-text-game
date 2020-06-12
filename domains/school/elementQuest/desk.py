import gametools
import container
import scenery

def clone():
    desk = container.Container('desk', __file__)
    desk.set_max_weight_carried(30000)
    desk.set_max_volume_carried(90)
    desk.set_description('sturdy desk', 'This is a sturdy desk made of dark oak behind it ther is a chair. It and everything on it is coated in a thin layer of dust, as if it hasn\'t been used in years.')
    desk.add_adjectives('sturdy', 'dark', 'oak')
    desk.add_names('table')

    prism = gametools.clone('domains.school.elementQuest.prism')
    desk.insert(prism)

    lamp = scenery.Scenery('lamp', 'antique lamp', 'This is an antique lamp with a buetiful shade that shows sollows flying over a lake.')
    lamp.add_adjectives('old', 'antique')
    lamp.add_response(['take','steel', 'replace'], 'Despite you best efforts you can not seem to take it. It is as if magic was holding it in place.')

    cracker_box = gametools.clone('domains.school.elementQuest.cracker_box')
    desk.insert(cracker_box)

    