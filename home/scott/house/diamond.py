import domains.wizardry.gems as gems

def clone():
    diamond = gems.Diamond(__file__, 'diamond', 'crystal-clear diamond', 'This diamond is hard to notice because it is so small.')
    return diamond