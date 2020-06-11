import creature
import thing

def clone():
    butterfly = creature.NPC('butterfly', __file__)
    butterfly.set_description('butterfly', 'A pretty monarch butterfly')
    butterfly.add_script("""wh""")
    return butterfly