import gametools
import container
import scenery
import thing

def clone():
    desk = container.Container('desk', __file__)
    desk.set_max_weight_carried(30000)
    desk.set_max_volume_carried(90)
    desk.set_description('sturdy desk', 'This is a sturdy desk made of dark oak behind it ther is a chair. It and everything on it is coated in a thin layer of dust, as if it hasn\'t been used in years.', unlisted=True)
    desk.add_adjectives('sturdy', 'dark', 'oak')
    desk.add_names('table')

    prism = gametools.clone('domains.school.elementQuest.prism')
    desk.insert(prism)

    lamp = scenery.Scenery('lamp', 'antique lamp', 'This is an antique lamp with a buetiful shade that shows sollows flying over a lake.')
    lamp.add_adjectives('old', 'antique')
    lamp.add_response(['take','steel', 'replace'], 'Despite you best efforts you can not seem to take it. It is as if magic was holding it in place.')

    cracker_box = gametools.clone('domains.school.elementQuest.cracker_box')
    cracker_box.plurality = 2
    desk.insert(cracker_box)

    pen = gametools.clone('domains.school.elementQuest.pen')
    pen.plurality = 3
    desk.insert(pen)

    blank_paper = gametools.clone('domains.school.elementQuest.paper')
    blank_paper.plurality = 13
    desk.insert(blank_paper)

    pencil = gametools.clone('domains.school.elementQuest.pencil')
    pencil.plurality = 6
    desk.insert(pencil)

    pencil_holder = gametools.clone('domians.school.elementQuest.pencil_holder')
    desk.insert(pencil_holder)

    tisue_box = gametools.clone('domains.renaissance_school.kleenex_box')
    desk.insert(tisue_box)

    hand_sanatizer = gametools.clone('domains.renaissance_school.hand_sanatizer')
    desk.insert(hand_sanatizer)


    return desk
