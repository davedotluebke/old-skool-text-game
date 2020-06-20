import asyncio
import json
import gametools

from thing import Thing

class AccessPoint(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.game = Thing.game
        self.user = None
        self.log = gametools.get_game_logger("_accesspoint")
        self.pending_commands = []
    
    def connection_lost(self, exc):
        # TODO: Implement code to deal with unexpected closures
        return super().connection_lost(exc)

    def data_received(self, data):
        try:
            message_dict = json.loads(data.decode('utf-8'))
        except Exception as e:
            self.log.exception('Invalid JSON message received! Printing below:')
            return
        try:
            message_type = message_dict['type']
        except KeyError as e:
            self.log.exception('message_dict missing `type` parameter!')
            return
        if message_type == "parse":
            if not self.user:
                self.log.error("Cannot create a pending command without a user!")
                return
            try:
                self.pending_commands.append(message_dict['message'])
            except KeyError as e:
                self.log.exception('message_dict missing `message` parameter!')
                return
        elif message_type == "load":
            if self.user:
                self.log.error("A user is already loaded. Please send an `unload` request before loading another user.")
                return
            try:
                self.user = self.game.load_player(message_dict['player_json'], self)
            except KeyError as e:
                self.log.exception('message_dict missing `player_json` parameter!')
                return
            except Exception as e:
                self.log.exception('An error occcured in load_player! Printing below:')
                return
        elif message_type == "save":
            if not self.user:
                self.log.error("There is no user loaded. Please send a `load` request to load a user.")
                return
            try:
                player_json = self.game.save_player(self.user, self)
                message = json.dumps({'type': 'save_return', 'player_json': player_json})
                self.transport.write(message.encode('utf-8'))
            except Exception as e:
                self.log.exception('An error occured in save_player! Printing below:')
                return
        elif message_type == "unload":
            if not self.user:
                self.log.error("There is no user loaded! Please send a `disconnect` request to diconnect.")
                return
            try:
                self.user.detach() # prints exit messages and destroys player
            except Exception as e:
                self.log.exception("An error occured detaching self.user! Printing below: ")
                return
        elif message_type == "disconnect":
            if self.user:
                self.log.error("Please call `unload` to detach self.user before disconnecting.")
                return
            self.transport.close()
        else:
            self.log.error("`message_type` must be `parse`, `load`, `save`, `unload`, or `disconnect`.")
            return
    
    def send_message(self, message):
        message_dict = {"type": "response", "message": message}
        message_json = json.dumps(message_dict)
        self.transport.write(message_json.encode('utf-8'))
