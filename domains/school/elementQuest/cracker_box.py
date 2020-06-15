import container
import gametools

def clone():
    cracker_box = container.Container('box', __file__)
    cracker_box.set_description('carboard cracker box', 'This is an ordinairy carboard cracker box. It\'s lable suggust that it once held some plain Nabisco® crackers.')
    cracker_box.set_max_volume_carried(1)
    cracker_box.set_max_weight_carried(200)
    cracker_box.set_weight(30)
    cracker_box.set_volume(1)
    cracker_box.add_adjectives('cracker', 'cardboard', 'ordinairy', 'Nabisco®', 'Nabisco', 'cracker')
    cracker_box.add_names('container')

    return cracker_box