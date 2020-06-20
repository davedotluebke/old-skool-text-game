# Console - Gameserver Communication
_Note: This file solely concerns interactions between the console and the gameserver. If you are only adding objects to the game, the contents of this file are of no relevance to you._
The communication between the console and the gameserver is done on a socket with port 9123. The communication on this socket consists of JSON objects (converted python dictionaries). Communication dictionaries from the console to the access point have the following parameters:
- `type`: The type of request: `load`, `parse`, `save`, `unload`, or `disconnect`.
  - If type is `load`, will load the player json from `player_json` and set `self.user` (where `self` is the `AccessPoint` object). If `self.user` is already set, will fail.
  - If type is `parse`, will call `Parser.parse()` on the string in `message` on a heartbeat. If `self.user` is not set, will fail.
  - If type is `save`, will save the player json from `self.user` to `player_json` and send it back. If `self.user` is not set, will fail.
  - If type is `unload`, will remove `self.user` from the server, including emiting decorative messages and calling `self.user.destroy()`. Sets `self.user` to `None` If `self.user` is not set, will fail. **Note: This does not save `self.user`.**
  - If type is `disconnect`, will terminate the connection. If `self.user` is set, will fail.
- `message`: The actual message string to be parsed upon heartbeat.
- `player_json`: The json object string representing the player. Used durring save and load calls.