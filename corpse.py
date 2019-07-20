import container

def clone(obj):
    corpse = container.Container("corpse", __file__)
    corpse.add_names("corpse")
    corpse.set_description('corpse of a %s' % (obj.short_desc), 'This is the foul-smelling corpse of a %s. It looks nasty.' % (obj.short_desc))
    corpse.set_weight(obj.get_weight())
    corpse.set_volume(obj.get_volume())
    corpse.set_max_weight_carried(obj.max_weight_carried)
    corpse.set_max_volume_carried(obj.max_volume_carried)
    corpse.add_names('corpse')
    return corpse
