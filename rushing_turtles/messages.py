from collections import namedtuple

import json

HelloServerMsg = namedtuple('HelloServerMsg', 'player_id,player_name')

TYPE_KEY = 'message'

class MessageDeserializer(object):

  def __init__(self):
    self.message_types = {
      'hello server': HelloServerMsg
    }

  def deserialize(self, msg_json : str):
    msg = json.loads(msg_json)
    if TYPE_KEY not in msg:
      raise ValueError(f"Invalid message: the message doesn't contain {TYPE_KEY} field")
    
    requested_type = msg.pop(TYPE_KEY)
    if requested_type not in self.message_types:
      raise ValueError(f"Invalid message: unrecognized message type: {requested_type}")
    
    msg_type = self.message_types[requested_type]
    missing_fields = [field for field in msg_type._fields if field not in msg]
    if missing_fields:
      raise ValueError(f"Invalid message: missing fields: " +
        ', '.join(missing_fields) + f" for message of type: {requested_type}")

    return msg_type(**msg)


class MsgToSend(object):
  
  def __init__(self, websocket, **kwargs):
    self.websocket = websocket
    self.content = json.dumps(kwargs)
  
  def __eq__(self, other):
    return self.content == other.content and self.websocket == other.websocket

  def __hash__(self):
    return hash((self.content, self.websocket))

  def __repr__(self):
    return f'MsgToSend({self.websocket}, {self.content})'
  
  async def send(self):
    await self.websocket.send(self.content)