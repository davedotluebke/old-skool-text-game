# Console - Gameserver Communication
_Note: This file solely concerns interactions between the console and the gameserver. If you are only adding objects to the game, the contents of this file are of no relevance to you._
The communication between the console and the gameserver is done on a socket with port 9123. The communication on this socket consists of JSON objects (converted python dictionaries). 
## Console to access point
Communication dictionaries from the console to the access point have the following parameters:
- `type`: The type of request: `load`, `parse`, `save`, `unload`, or `disconnect`.
  - If type is `load`, the AccessPoint will load the player json from `player_json` and set `self.user` (where `self` is the `AccessPoint` object). If `self.user` is already set, will fail.
  - If type is `parse`, the AccessPoint will call `Parser.parse()` on the string in `message` on a heartbeat. If `self.user` is not set, will fail.
  - If type is `save`, the AccessPoint will save the player json from `self.user` to `player_json` and send it back. If `self.user` is not set, will fail.
  - If type is `unload`, the AccessPoint will remove `self.user` from the server, including emiting decorative messages and calling `self.user.destroy()`. Sets `self.user` to `None` If `self.user` is not set, will fail. **Note: This does not save `self.user`.**
  - If type is `disconnect`, the AccessPoint will terminate the connection. If `self.user` is set, will fail.
- `message`: The actual message string to be parsed upon heartbeat.
- `player_json`: The json object string representing the player. Used during save and load calls.

The correct way to logout a player is therefore to make a `save` request, then an `unload` request, then a `disconnect` request.

## Access point to console
Dictionaries going the other way have the following paramaters:
- `type`: The type of request: `error`, `response`, or `save_return`.
  - If type is `response`, the `message` attribute contains a message for the client.
  - If type is `save_return`, the `player_json` attribute contains a player json, returned for saving.
  - If type is `error`, an error has occurred in the execution of the console's request This will *NOT* happen if the user tried to do something illegal (e.g. `read table`, `attack the nonexistent monster`), but instead if there is an error in the code somewhere that causes the request to be uncompleteable (e.g. `print'hi')`). The error code will be set and the `message` attribute should contain a human-readable description of what went wrong.
- `message`: The message to be written to the client.
- `player_json`: The json object string representing the player. Returned from save calls.
- `error-code`: If 0, success. Otherwise, this is a number readable by the console so it can tell what went wrong. Error codes are defined in `gametools.py`.
