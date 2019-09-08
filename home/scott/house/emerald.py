import domains.wizardry.gems as gems

def clone():
    emerald = gems.Emerald(__file__, 'emerald', 'delecately cut emerald', 'This is a delicately cut emerald.', power_num=100)
    return emerald
