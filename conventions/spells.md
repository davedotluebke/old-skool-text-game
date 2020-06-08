For general information on how spells work, please see GitHub issue [#85](https://github.com/davedotluebke/old-skool-text-game/issues/85). 
This file is on how spells are treated in-game.
# Spells
## In general
To cast a spell, the player types `cast <spellname> <spellinfo>`. 
`<spellname>` is the name of the spell and `<spellinfo>` is
information that the spell needs, for example a duration or an 
object to use the spell on. For example, `cast illuminate 5` would
cast the spell illuminate for 5 seconds.
## Parts of a spell
Each spell has, at the minimum, a `get_mana()` function that returns the mana required for a spell
and a `spell` function that actually runs the spell. Both take the arguments
`parser`, `cons`, `oDO`, `oIDO`, and `spell_info`. `spell_info` is a list
of everything after the `cast <spellname>` as shown above and is equivalent to
`parser.words[2:]`. 