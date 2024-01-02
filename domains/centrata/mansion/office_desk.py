import container
import gametools

def clone():
    desk = container.Container('desk', __file__)
    desk.set_description('carved mahogany desk', 'This carved mahogany desk is small for a desk, but intricately detailed. You notice patterns of fruits around the edges.', unlisted=True)
    desk.fix_in_place('The desk is too heavy and awkward to move.')
    desk.add_adjectives('carved', 'mahogany')
    desk.set_prepositions('on', 'onto', 'in', 'into')
    desk.set_max_weight_carried(4e9)
    desk.set_max_volume_carried(80)

    paper = gametools.clone('domains.centrata.mansion.office_paper')
    paper.plurality = 60
    desk.insert(paper, True)

    pen = gametools.clone('domains.centrata.mansion.office_pen')
    desk.insert(pen, True)

    return desk
