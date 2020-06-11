import armor
import thing
import gametools

def clone():
    chain_mail = armor.Armor('armor', __file__, 45, 3)
    chain_mail.set_description('chain mail suit', 'armor', 'This is a though but heavy chain mail suit, it shines in the light.')
    chain_mail.add_adjectives('chain', 'mail', 'though', 'heavy', 'metal', 'suit', 'armor')
    chain_mail.add_names('mail', 'post', 'suit', 'armour')
    chain_mail.set_volume(5)
    chain_mail.set_weight(13000)

    return chain_mail