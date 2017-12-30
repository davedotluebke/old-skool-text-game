# old-skool-text-game
Coding project used by Owen (and Dave) to learn Python

Contains a framework somewhat like the old LPMud worlds (see genesismud.org):

## The World
The world consists of a scorcery school, where you are assigned quests with a magical scroll. Your quests may take you into dangerous forests, pit you against fierce monsters, teach you to brew new types of potions, etc. Eventual goal is that players will be able to become wizards and add their own quests, monsters, etc. to the world.

## Playing the game
Players play the game by typing commands such as `take the rusty sword` and `go north`. Their command is parsed and the text result is printed to their console.

## Coding
The coding of the game is primarily in python 3, and hosts a server that players can log onto using telnet. The server is writen using twisted (twistedmatrix.com) and allows multiple players to log on and interact using asynchronous operation. 

## Installation (Linux)
> _These instructions were tested on Linux Mint 18 which is based on Ubuntu 16.04. Other flavors of Linux may follow similar steps_

**NOTICE:** This game is in the early stages of development and, therefore, is prone to buggy behavior and is rampant with half finished content. These instructions are here primarily for those who are either interested in contributing or simply curious to see how the project is progressing. Do not install this expecting to find a completed and polished game just yet. That is still a ways down the road.

### Dependency installation 
```
sudo apt-get install python3 python3-dev python3-pip

# upgrade pip
sudo pip3 --upgrade pip

# install twisted.internet
sudo pip3 install setuptools
sudo pip3 install twisted[tls]

# check for unmet dependencies
pip3 check

# fix any unmet dependencies
sudo pip3 install cryptography
sudo pip3 install pyasn1-modules
```
Please note that unmet dependencies revealed by the `pip3 check` command may be reliant on each other. As such, if one refuses to update, it may be because another must be updated first. Try installing the rest, and then retry any that had failed previously.

### Downloading the source code
If you have git installed on your computer you can clone the git repository to your hard drive by opening a terminal to the folder you wish to keep it in and typing:

`git clone https://github.com/davedotluebke/old-skool-text-game.git`

Alternatively, you can:
1. Go to [https://github.com/davedotluebke/old-skool-text-game](https://github.com/davedotluebke/old-skool-text-game)
2. Click the green button that says "Clone or download"
3. Select "Download ZIP"
4. Extract the files wherever you want the game to be located.

### Running the game
This is a server game, and as such, you must first start a server application and then connect to it as a client.

#### Starting the server
To start the game server, open a terminal to the git source directory and type:

`python3 OAD.TextGame.py`

#### Joining the server
telnet:
> Telnet is the simplest way to connect but does have its drawbacks. For instance, if the server displays a message while you are typing, the screen will scroll, taking half of your command string with it. That will prevent you from using `<backspace>` to make changes to what you've already typed.

To join the game server using `telnet`, simply open another terminal and type:

`telnet localhost 9123`

***

[kbtin](https://github.com/kilobyte/kbtin):

> Kbtin is a terminal-based MUD client. It comes packed with many features, but the simplest and greatest is simply that it prevents the output from the server from interfering with the commands you are typing.

To install kbtin, type:

`sudo apt-get install kbtin`

For convenience you may wish to create a short script file for loading the game. In your home directory, create a file called `oad`. In it, put the following:

```
#charset UTF-8
#session OAD localhost 9123
```

In order to join the server, open a terminal to your home folder and type:

`kbtin oad`

