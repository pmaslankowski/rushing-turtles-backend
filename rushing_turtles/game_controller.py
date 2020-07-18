import logging


from typing import List

from rushing_turtles.messages import  MsgToSend
from rushing_turtles.messages import HelloServerMsg
from rushing_turtles.messages import WantToJoinMsg
from rushing_turtles.messages import StartGameMsg
from rushing_turtles.model.person import Person

# TODO: upewnić się, że pid przysłany przez playera zgadza się z websocketem
class GameController(object):
  
  def __init__(self):
    self.ws2pid = {}
    self.lounge = []
    self.room = []
    self.game = None

  def handle(self, msg, websocket) -> List[MsgToSend]:
    if isinstance(msg, HelloServerMsg):
      return self._handle_hello_server(msg, websocket)
    elif isinstance(msg, WantToJoinMsg):
      return self._handle_want_to_join(msg, websocket)
    elif isinstance(msg, StartGameMsg):
      return self._handle_start_game(msg, websocket)
    else:
      logging.warning(f'Unhandled message: {msg}')


  def _handle_hello_server(self, msg : HelloServerMsg, websocket):
    if self._is_person_already_connected(msg.player_id):
      raise ValueError(f'Person with id = {msg.player_id} is already' +
                          'connected to the server')

    self.ws2pid[websocket] = msg.player_id
    person = Person(msg.player_id, msg.player_name)
    self.lounge.append(person)
    
    if not self.room:
        return MsgToSend(websocket,
          message='hello client',
          status='can create', 
          list_of_players_in_room=[])
    else:
      return MsgToSend(websocket, 
        message='hello client',
        status='can join',
        list_of_players_in_room=[person.name for person in self.room])
  
  def _is_person_already_connected(self, id : int):
    return id in self.ws2pid 

  def _handle_want_to_join(self, msg: WantToJoinMsg, websocket):
    if msg.status == 'create the game':
      person = self._find_person_in_lounge(msg.player_id)
      if self.room:
        raise ValueError('Room is already created')

      self.lounge.remove(person)
      self.room.append(person)

      return self._broadcast_room_update()
    elif msg.status == 'join the game':
      if not self.room:
        raise ValueError('Room does not exist yet')
      
      person = self._find_person_in_lounge(msg.player_id)
      self.lounge.remove(person)
      self.room.append(person)

      return self._broadcast_room_update()

  def _broadcast_room_update(self):
    return [MsgToSend(ws, 
        message='room update', 
        list_of_players_in_room=[person.name for person in self.room]
        ) for ws in self.ws2pid.keys()]
  
  def _find_person_in_lounge(self, id : int):
    for person in self.lounge:
      if person.id == id:
        return person
    raise ValueError(f'Person with id = {id} is not in lounge')
  
  def _handle_start_game(self, msg : StartGameMsg, websocket):
    idx_in_room = self._find_person_idx_in_room(msg.player_id)
    if idx_in_room != 0:
      raise ValueError(f'Person with id = {id} is not the first person in the room' +
                        ' so they cannot start the game')

  def _find_person_idx_in_room(self, id: int):
    for idx, person in enumerate(self.room):
      if person.id == id:
        return idx
    raise ValueError(f'Person with id = {id} is not in the room')