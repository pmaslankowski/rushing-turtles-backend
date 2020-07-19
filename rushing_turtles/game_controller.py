import logging


from typing import List

from rushing_turtles.messages import  MsgToSend
from rushing_turtles.messages import HelloServerMsg
from rushing_turtles.messages import WantToJoinMsg
from rushing_turtles.messages import StartGameMsg
from rushing_turtles.model.person import Person

MAX_PLAYERS_IN_ROOM = 5

class GameController(object):
  
  def __init__(self):
    self.people = []
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

    person = Person(msg.player_id, msg.player_name, websocket)
    self.people.append(person)
    
    if not self.room:
        return MsgToSend(websocket,
          message='hello client',
          status='can create', 
          list_of_players_in_room=[])
    elif len(self.room) < MAX_PLAYERS_IN_ROOM:
      return MsgToSend(websocket, 
        message='hello client',
        status='can join',
        list_of_players_in_room=[person.name for person in self.room])
    else:
      return MsgToSend(websocket, 
        message='hello client', 
        status='limit',
        list_of_players_in_room=[person.name for person in self.room])

  def _is_person_already_connected(self, id : int):
    return id in [person.id for person in self.people]

  def _handle_want_to_join(self, msg: WantToJoinMsg, websocket):
    pid = msg.player_id
    person = self._find_person(pid)
    self._ensure_that_player_not_poses_as_somebody_else(person, websocket)

    if msg.status == 'create the game':
      if self.room:
        raise ValueError('Room is already created')
      self.room.append(person)
      return self._broadcast_room_update() + \
        self._broadcast_can_join_except_pid(pid)
        
    elif msg.status == 'join the game':
      if not self.room:
        raise ValueError('Room does not exist yet')
      if len(self.room) >= MAX_PLAYERS_IN_ROOM:
        raise ValueError('Room is full')
      if person in self.room:
        raise ValueError(f'Person {person} is already in the room')

      self.room.append(person)

      return self._broadcast_room_update()

  def _ensure_that_player_not_poses_as_somebody_else(self, person, websocket):
    if person.websocket != websocket:
      raise ValueError(f"You can't play as player {person} - " + 
                        "he is already controlled by someone else")

  def _broadcast_room_update(self):
    return self._broadcast(lambda ws: 
      MsgToSend(ws, 
        message='room update', 
        list_of_players_in_room=self._get_names_of_players_in_room()
      ))

  def _broadcast(self, producer):
    return [producer(person.websocket) for person in self.people]

  def _get_names_of_players_in_room(self):
    return [person.name for person in self.room]

  def _broadcast_can_join_except_pid(self, pid):
    return self._broadcast_except(lambda ws:
      MsgToSend(ws, 
        message='hello client',
        status='can join',
        list_of_players_in_room=self._get_names_of_players_in_room()
      ), pid)

  def _broadcast_except(self, producer, pid):
    return [producer(person.websocket) for person in self.people if person.id != pid]
  
  def _find_person(self, id : int):
    for person in self.people:
      if person.id == id:
        return person
    raise ValueError(f'Person with id = {id} is not connected')
  
  def _handle_start_game(self, msg : StartGameMsg, websocket):
    pid = msg.player_id
    person = self._find_person(pid)
    self._ensure_that_player_not_poses_as_somebody_else(person, websocket)

    if person not in self.room:
      raise ValueError(f'Person {person} is not in the room')
    if self.room[0] != person:
      raise ValueError(f'Person {person} is not the first player in the room' +
                        ' so he cannot start the game')

  def disconnected(self, websocket):
    person = self._find_person_by_websocket(websocket)
    self.people.remove(person)
    if person in self.room:
      self.room.remove(person)
      return self._broadcast_room_update()

  def _find_person_by_websocket(self, websocket):
    for person in self.people:
      if person.websocket == websocket:
        return person
    raise ValueError(f'There is no person corresponding to given websocket: {websocket}')