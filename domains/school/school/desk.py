import container
import gametools

def clone():
    desk = container.Container('desk', __file__)
    desk.set_description('carved oak desk', 'This carved oak desk is clearly more than 100 years old, and is carved out in the shapes of dragons and other vicious creatures. There are a few papers on its surface.', unlisted=True)
    desk.fix_in_place('The desk is very, very heavy, and feels rooted to the floor.')
    desk.add_adjectives('carved', 'oak')
    desk.set_prepositions('on', 'onto', 'in', 'into')
    desk.set_max_weight_carried(4e9)
    desk.set_max_volume_carried(80)

    paper_one = gametools.clone('domains.school.school.paper_one')
    paper_two = gametools.clone('domains.school.school.paper_two')
    paper_three = gametools.clone('domains.school.school.paper_three')
    desk.insert(paper_one, True)
    desk.insert(paper_two, True)
    desk.insert(paper_three, True)

    return desk
