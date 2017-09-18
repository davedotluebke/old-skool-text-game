import domains.wizardry.deep_pocket.classes as classes

def clone():
    vaults = classes.VaultRoom("Vaults")
    vaults.set_description("vault entrance", "This small room serves as the entrence to all of the vaults.")
    return vaults
