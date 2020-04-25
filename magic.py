import importlib
import gametools

def castChecks(player, parser, cons, oDO, oIDO):
    specifications = parser.words[2:]
    try:
        path = player.spellsKnown[parser.words[1]]
    except KeyError:
        return "You don't know any spell called %s!" % parser.words[1]
    return cast(parser, cons, oDO, oIDo, path, specifications)
    
def cast(parser, cons, oDO, oIDO, path, spell_info=[]):
    try:
        lib = importlib.import_module(path)
    except ModuleNotFoundError:
        return 'That spell does not exist!'
    except ImportError as e:
        cons.write('Something went wonky with loading your spell.')
        cons.user.log.error(e)
        return True
    try:
        mana = lib.get_mana(parser, cons, oDO, oIDO, spell_info)
    except gametools.BadSpellInfoError as e:
        cons.write(e.args[0])
        return True
    # TODO: deal with mana here
    try:
        return lib.spell(parser, cons, oDO, oIDO, spell_info)
    except gametools.BadSpellInfoError as e:
        cons.write(e.args[0])
        return True
    except Exception as e:
