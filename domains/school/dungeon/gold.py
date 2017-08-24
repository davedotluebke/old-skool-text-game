import domains.school.trapthings as trapthings

def clone():
    gold = trapthings.TrapThing('gold', __file__, 'You try to take the gold but a trap is sprung! You fall into a deep pit...', 'domains.school.dungeon.pit', 'goldtrap9125')
    gold.set_description('bunch of shiny gold coins', 'This is a collection of 50 shiny real gold coins.')
    gold.set_weight(74000)
    return gold
