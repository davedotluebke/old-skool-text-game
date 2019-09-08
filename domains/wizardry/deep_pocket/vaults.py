import domains.wizardry.deep_pocket.classes as classes
import room
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    vaults = classes.VaultRoom("Vaults", pref_id=roomPath)
    vaults.set_description("vault entrance", "This small room serves as the entrance to all of the vaults.")
    return vaults
