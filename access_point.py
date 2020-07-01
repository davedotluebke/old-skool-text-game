import asyncio
import json
import gametools
import traceback

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
            self.send_message('Invalid JSON message received!', 401)
            return
        try:
            message_type = message_dict['type']
        except KeyError as e:
            self.log.exception('message_dict missing `type` parameter!')
            self.send_message('message_dict missing `type` parameter!', 400)
            return
        if message_type == "parse":
            if not self.user:
                self.log.error("Cannot create a pending command without a user!")
                self.send_message("Cannot create a pending command without a user!", 406)
                return
            try:
                self.pending_commands.append(message_dict['message'])
            except KeyError as e:
                self.log.exception('message_dict missing `message` parameter!')
                self.send_message('message_dict missing `message` parameter!', 400)
                return
        elif message_type == "load":
            if self.user:
                self.log.error("A user is already loaded. Please send an `unload` request before loading another user.")
                self.send_message("A user is already loaded. Please send an `unload` request before loading another user.", 406)
                return
            try:
                self.user = self.game.load_player(message_dict['player_json'], self)
                self.user.access_point = self
            except KeyError as e:
                self.log.exception('message_dict missing `player_json` parameter!')
                self.send_message('message_dict missing `player_json` parameter!', 400)
                return
            except Exception as e:
                self.log.exception('An error occcured in load_player! Printing below:')
                self.send_message(traceback.format_exc(), 501)
                return
        elif message_type == "save":
            if not self.user:
                self.log.error("There is no user loaded. Please send a `load` request to load a user.")
                self.send_message("There is no user loaded. Please send an `load` request before loading another user.", 406)
                return
            try:
                player_json = self.game.save_player(self.user, self)
                message = json.dumps({'type': 'save_return', 'player_json': player_json})
                self.transport.write(message.encode('utf-8'))
            except Exception as e:
                self.log.exception('An error occurred in save_player! Printing below:')
                self.send_message(traceback.format_exc(), 501)
                return
        elif message_type == "unload":
            if not self.user:
                self.log.error("There is no user loaded! Please send a `disconnect` request to diconnect.")
                self.send_message("There is no user loaded! Please send a `disconnect` request to diconnect.", 406)
                return
            try:
                self.user.detach() # prints exit messages and destroys player
            except Exception as e:
                self.log.exception("An error occurred detaching self.user! Printing below: ")
                self.send_message(traceback.format_exc(), 501)
                return
        elif message_type == "disconnect":
            if self.user:
                self.log.error("Please call `unload` to detach self.user before disconnecting.")
                self.send_message("Please call `unload` to detach self.user before disconnecting.", 406)
                return
            self.transport.close()
        else:
            self.log.error("`message_type` must be `parse`, `load`, `save`, `unload`, or `disconnect`.")
            self.send_message("`message_type` must be `parse`, `load`, `save`, `unload`, or `disconnect`.", 400)
            return
    
    def send_message(self, message, error=0):
        message_type = "response" if not error else "error"
        message_dict = {"type": message_type, "message": message, 'error_code': error}
        message_json = json.dumps(message_dict)
        self.transport.write(message_json.encode('utf-8'))
