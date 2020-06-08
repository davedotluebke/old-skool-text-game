import container
import gametools

def clone():
    flyer_box = container.Container('box', __file__)
    flyer_box.set_description('flyer box', 'This is a flyer box, filled with various different flyers about the school.')
    flyer_box.add_adjectives('flyer', 'school')

    for i in range(0, 10):
        flyer = gametools.clone('domains.renaissance_school.random_flyer')
        flyer.move_to(flyer_box, True)

    flyer_box.fix_in_place('The flyer box is attached to the wall.')
    return flyer_box
