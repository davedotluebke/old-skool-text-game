# Webclient - Console Communication
_Note: This file solely concerns interactions between the webclient and the console. If you are only adding objects to the game, the contents of this file are of no relevance to you._

The communication between the webclient and the console is handled on two different connections - a websocket from the client to the console overseer, and a socket from the console overseer to the console. The communication consists of JSON objects (converted javascript objects / python dictionaries).
## The console overseer
The console overseer itself responds to the dictionaries sent before a connection is made. This dictionary is expected to have the following paramaters:
- `type`: `'login'`
- `data`: the username to connect to

The console overseer has a list of users and their passwords. If the username is not in the file, then the following dictionary is returned:
- `type`: `'confirmation'`
- `data`: a question asking if the person would like to create a new user with the given name

If the above question is answered `yes`, then the following message is sent.
- `type`: `password_request`
- `data`: `Please create a password:`

If the user already exits, instead the following will happen.

The console overseer also stores a mapping of the websocket to the username. If an entry with the specified username already exists, it will return this dictionary:
- `type`: `confirmation`
- `data`: a message asking for confirmation on taking over the connection from the username specified

Otherwise, or follwing positive confirmation to the above message, the following dictionary will be returned to the webclient:
- `type`: `'password_request'`
- `data`: `'Please enter your --#password:'`

The response expected to this is:
- `type`: `'password'`
- `data`: the user's password (already hashed)

The user's password is hashed once again upon arrival, and is checked against the stored password hash. If they match, then:
- If the username is a wizard, we start a console in the appropriate user. 
- Otherwise, we start the console in the `nwconsole` user.

### Console to Console Overseer Connection
When the Console starts, it creates a socket connection to the Console Overseer on port 9125. It sends a message dictionary containing its username and a random hash that was passed to it on startup. From this point on, all messages are simply forwarded through the Console Overseer to the Console.

When the connection between the console and the console overseer is closed, the websocket connection is also closed.

## Forwarded communication
The following is a description of the communication directly between the webclient and the console.

Below are valid messages for the webclient to send to the console:
- `type`: `command`
- `data`: An input string for the console to parse

- `type`: `file`
- `data`: A file for the console to save
- `filename`: The filename to save the file as

Below are valid messages for the console to send to the webclient:
- `type`: `response`
- `data`: Something to be printed to the user's screen

- `type`: `file`
- `data`: The contents of a file
- `behaviour`: Whether to save the file or open an editor
- `filename`: The name of the file