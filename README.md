# old-skool-text-game
Coding project used by Owen (and Dave) to learn Python

Contains a framework somewhat like the old LPMud worlds (see genesismud.org):

## The World
The world consists of a scorcery school, where you are assigned quests with a magical scroll. Your quests may take you into dangerous forests, pit you against fierce monsters, teach you to brew new types of potions, etc. Eventual goal is that players will be able to become wizards and add their own quests, monsters, etc. to the world.

## Playing the game
Players play the game by typing commands such as `take the rusty sword` and `go north`. Their command is parsed and the text result is printed to their console.

## Coding
The coding of the game is primarily in python 3, and hosts a server that players can log onto using telnet. The server is writen using twisted (twistedmatrix.com) and allows multiple players to log on and interact using asynchronous operation. 
