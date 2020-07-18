import logging


from typing import List

from rushing_turtles.messages import HelloServerMsg, MsgToSend
from rushing_turtles.model.person import Person


class GameController(object):
  
  def __init__(self):
    self.lounge = {}
    self.room = {}
    self.game = None

  def handle(self, msg, websocket) -> List[MsgToSend]:
    print(msg)
    if isinstance(msg, HelloServerMsg):
      if not self.room:
        person = Person(msg.player_id, msg.player_name)
        self.lounge[person.id] = person
        return MsgToSend(websocket,
          message='hello client',
          status='can create', 
          list_of_players_in_room=[])
      else:
        return MsgToSend(websocket, 
          message='hello client',
          status='can join',
          list_of_players_in_room=[person.name for person in self.room])
    if msg['message'] == 'want to join game':
      if msg['status'] == 'create_the_game':
        pass
    else:
      logging.warning(f'Unhandled message: {msg}')