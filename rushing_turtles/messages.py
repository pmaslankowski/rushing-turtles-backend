from collections import namedtuple

import json

HelloServerMsg = namedtuple('HelloServerMsg', 'player_id, player_name')
WantToJoinMsg = namedtuple('WantToJoinTheGame', 'player_id')
StartGameMsg = namedtuple('StartGame', 'player_id')
ReadyToReceiveGameState = namedtuple('ReadyToReceiveGameState', 'player_id')
PlayCardMsg = namedtuple('PlayCardMsg', 'player_id, card_id, picked_color')

TYPE_KEY = 'message'


class MessageDeserializer(object):

    def __init__(self):
        self.message_types = {
          'hello server': HelloServerMsg,
          'want to join the game': WantToJoinMsg,
          'start the game': StartGameMsg,
          'ready to receive game state': ReadyToReceiveGameState,
          'play card': PlayCardMsg
        }

    def deserialize(self, msg_json: str):
        msg = json.loads(msg_json)
        msg_type, msg_type_as_str = self._extract_message_type(msg)

        missing_fields = [field for field in msg_type._fields
                          if field not in msg]
        if missing_fields:
            raise ValueError("Invalid message: missing fields: " +
                             ', '.join(missing_fields) +
                             f" for message of type: {msg_type_as_str}")

        return msg_type(**msg)

    def _extract_message_type(self, msg):
        if TYPE_KEY not in msg:
            raise ValueError("Invalid message: " +
                             f"the message doesn't contain {TYPE_KEY} field")

        requested_type = msg.pop(TYPE_KEY)
        if requested_type not in self.message_types:
            raise ValueError("Invalid message: " +
                             f"unrecognized message type: {requested_type}")

        return self.message_types[requested_type], requested_type


class MsgToSend(object):

    def __init__(self, websocket, **kwargs):
        self.websocket = websocket
        self.type = kwargs['message']
        self.content = json.dumps(kwargs)

    def __eq__(self, other):
        return self.content == other.content and \
          self.websocket == other.websocket and \
          self.type == other.type

    def __hash__(self):
        return hash((self.type, self.content, self.websocket))

    def __repr__(self):
        return f'MsgToSend({self.websocket}, {self.type}, {self.content})'

    async def send(self):
        await self.websocket.send(self.content)
