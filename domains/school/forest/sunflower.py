import domains.school.flower as flowerMod
import action

def clone():
    sunflower = flowerMod.Flower("sunflower", __file__, 'sunflower')
    sunflower.set_description("giant sunflower" , "By looking at this giant sunflower you start feeling more happy.")
    sunflower.set_volume(3)
    sunflower.set_weight(200)
    sunflower.add_adjectives('happiness','giant')
    return sunflower
