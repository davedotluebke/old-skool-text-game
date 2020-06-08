import container
import gametools

def clone():
    rusty_can = container.Container('can', __file__)
    rusty_can.set_description('rusty can', 'This is a rusty canister, now discarded. It\'s large enough to hold something inside.')
    rusty_can.add_adjectives('rusty', 'oil')
    rusty_can.set_weight(2000)
    rusty_can.set_volume(20)
    rusty_can.set_max_volume_carried(20)
    rusty_can.set_max_weight_carried(10000)

    kinfe = gametools.clone('domains.school.elementQuest.knife')
    rusty_can.insert(kinfe, True)
    
    return rusty_can
