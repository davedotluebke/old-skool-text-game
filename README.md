# old-skool-text-game
A text adventure game written in Python.

## The World
Players start their journey in a scorcery school, where they are assigned quests with a magical scroll. As they continue to play, their quests may take them into dangerous forests, pit them against fierce monsters, teach them to brew new types of potions, and more. Players can become wizards who are able to change the very world itself.

## Playing the game
Players play the game by typing commands such as `take the rusty sword` and `go north`. Players can then see the result of their interactions.

## Coding
The coding of the game is primarily in [Python 3](python.org), and hosts a server that players can log onto using a web interface. The server is writen using websockets and allows multiple players to log on and interact using asynchronous operation. 

## Documentation
Documentation for wizards to create their own rooms, objects, and so on is located in the conventions folder. See [conventions/conventions.md](conventions/conventions.md) for more information.

## Launching the game
### Connecting to the global server
To connect to the global server, go to [firefile.us](firefile.us) and click on "Begin playing." Then, press enter.
### Hosting a server locally
Sometimes, it is useful to host the game locally for development or offline play. To do this, clone the git directory to your machine. Then, try to run `startup.py`. You will almost inevitably get a string of `ModuleNotFound` errors. Install these modules. Once the game prompts you for an IP address, enter `127.0.0.1`. Then, go to [firefile.us](firefile.us), click "Begin playing," and enter `127.0.0.1` as your IP address. If you are offline and cannot access [firefile.us](firefile.us), then (in a seperate terminal from `startup.py`) go into the [webclient folder](webclient) and run `python3 -m http.server`. Then, go to [http://localhost:8000](http://localhost:8000).