import importlib
import gametools
from random import random

def castChecks(player, parser, cons, oDO, oIDO):
    if len(parser.words) < 2:
        return "Usage: Cast <spell> [parameters] [with <stone>]"
    specifications = parser.words[2:]
    try:
        path = player.spellsKnown[parser.words[1]]
    except KeyError:
        return "You don't know any spell called %s!" % parser.words[1]
    wordstring = ' '.join(parser.words)
    try:
        withindex = wordstring.rindex('with')
        return cast(parser, cons, oDO, oIDO, path, specifications, usingstone=True)
    except ValueError:
        return cast(parser, cons, oDO, oIDO, path, specifications)

def cast(parser, cons, oDO, oIDO, path, spell_info=[], usingstone=False):
    try:
        lib = importlib.import_module(path)
    except ModuleNotFoundError:
        return 'That spell does not exist!'
    except ImportError as e:
        cons.write('Something went wonky with loading your spell.')
        cons.user.log.error(e)
        return True
    try:
        origMana = lib.get_mana(parser, cons, oDO, oIDO, spell_info, None)
    except gametools.BadSpellInfoError as e:
        cons.write(e.args[0])
        return True
    mana = origMana
    stone = None
    if usingstone:
        wordstring = ' '.join(parser.words)
        withindex = wordstring.rindex('with') + 4
        possible_stones = parser.find_matching_objects(wordstring[withindex:], parser._collect_possible_objects(cons.user), cons)
        if possible_stones == False:
            return True
        elif not possible_stones:
            return "I can't find any %s to cast with!" % wordstring[withindex:]
        for stone in possible_stones:
            stone_mana = stone.get_mana()
            new_stone_mana = stone_mana - mana
            if new_stone_mana < 0:
                new_stone_mana = 0
                mana -= stone_mana
            else:
                mana = 0
            if mana <= cons.user.mana:
                cons.user.mana -= mana
            else:
                cons.write("You don't have enough mana to cast this spell.")
                return True
            stone.set_mana(new_stone_mana)
    else:    
        if mana <= cons.user.mana:
            cons.user.mana -= mana
        else:
            cons.write("You don't have enough mana to cast this spell.")
            return True
    try:
        messUp = random()
        if messUp <= cons.user.calc_chance_mess_up(origMana):
            #They messed up
            if hasattr(lib, "bad_spell") and callable(lib.bad_spell):
                return lib.bad_spell(parser, cons, oDO, oIDO, spell_info, stone, (messUp - cons.user.calc_chance_mess_up(origMana)))
        return lib.spell(parser, cons, oDO, oIDO, spell_info, stone)
    except gametools.BadSpellInfoError as e:
        cons.write(e.args[0])
        return True
    except Exception as e:
        cons.user.log.error(e)
        cons.write('An error occured in casting the spell!')
        return True
