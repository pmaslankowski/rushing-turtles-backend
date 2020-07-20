import logging


from typing import List

from rushing_turtles.messages import MsgToSend
from rushing_turtles.messages import HelloServerMsg
from rushing_turtles.messages import WantToJoinMsg
from rushing_turtles.messages import StartGameMsg
from rushing_turtles.messages import ReadyToReceiveGameState
from rushing_turtles.messages import PlayCardMsg
from rushing_turtles.model.person import Person
from rushing_turtles.model.game import Game, create_game
from rushing_turtles.model.board import Board
from rushing_turtles.model.card import Card
from rushing_turtles.model.action import Action

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
    elif isinstance(msg, ReadyToReceiveGameState):
      return self._handle_ready_to_receive_game_state(msg, websocket)
    elif isinstance(msg, PlayCardMsg):
      return self._handle_play_card(msg, websocket)
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
    elif not self.game and len(self.room) < MAX_PLAYERS_IN_ROOM:
      return MsgToSend(websocket, 
        message='hello client',
        status='can join',
        list_of_players_in_room=self._get_names_of_players_in_room())
    elif self.game:
      return MsgToSend(websocket,
        message='hello client',
        status='ongoing',
        list_of_players_in_room=self._get_names_of_players_in_room())
    else:
      return MsgToSend(websocket, 
        message='hello client', 
        status='limit',
        list_of_players_in_room=self._get_names_of_players_in_room())

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
      if self.game:
        raise ValueError(f'Game has already started')

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

    self.game = create_game(self.room)    
    return self._emit_ongoing_to_players_outside_the_room() + \
      self._emit_game_ready_to_start_to_players_in_room()

  def _emit_ongoing_to_players_outside_the_room(self):
    return [MsgToSend(person.websocket, 
        message='hello client',
        status='ongoing',
        list_of_players_in_room=self._get_names_of_players_in_room()
      ) for person in self.people if person not in self.room]
  
  def _emit_game_ready_to_start_to_players_in_room(self):
    return [MsgToSend(person.websocket,
        message='game ready to start', 
        player_idx=self.game.get_person_idx(person)
      ) for person in self.room]
  
  def _handle_ready_to_receive_game_state(self, msg: ReadyToReceiveGameState, websocket):
    pid = msg.player_id
    person = self._find_person(pid)
    self._ensure_that_player_not_poses_as_somebody_else(person, websocket)
    if not self.game:
      raise ValueError('Game has not started yet')
    
    player = self.game._find_player(person)
    return MsgToSend(websocket,
      message='full game state',
      board=self._board_to_dict(self.game.board),
      players_names=self._get_names_of_players_in_room(),
      active_player_idx=self.game._find_player_idx(self.game.active_player),
      player_cards=[self._card_to_dict(card) for card in player.cards],
      player_turtle_color=player.turtle.color,
      recently_played_card=self._card_to_dict(self.game.stacks.get_recent())
    )
  
  def _board_to_dict(self, board : Board):
    return {
      'turtles_in_game_positions': [[str(turtle) for turtle in stack] 
        for stack in board.further_fields],
      'turtles_on_start_positions': [[str(turtle) for turtle in stack]
        for stack in board.start_field]
    }  

  def _card_to_dict(self, card : Card):
    if not card:
      return None
    return {'card_id': card.id, 'color': card.color, 'action': card.symbol}

  def _handle_play_card(self, msg : PlayCardMsg, websocket):
    pid = msg.player_id
    person = self._find_person(pid)
    self._ensure_that_player_not_poses_as_somebody_else(person, websocket)

    if not self.game:
      raise ValueError('The game has not started yet')
    
    card = self.game.get_card(msg.card_id)
    action = Action(card, msg.picked_color)
    self.game.play(person, action)
    new_cards = self.game.get_persons_cards(person)

    game_state_updated_msgs = self._broadcast(lambda ws: MsgToSend(ws,
      message='game state updated',
      board=self._board_to_dict(self.game.board),
      active_player_idx=self.game._find_player_idx(self.game.active_player),
      recently_played_card=self._card_to_dict(self.game.stacks.get_recent())
    ))

    player_cards_updated_msg = [MsgToSend(websocket, 
      message='player cards updated',
      player_cards=[self._card_to_dict(card) for card in new_cards])]

    return game_state_updated_msgs + player_cards_updated_msg

  def disconnected(self, websocket):
    person = self._find_person_by_websocket(websocket)
    self.people.remove(person)
    #if person in self.room:
    #  self.room.remove(person)
    #  return self._broadcast_room_update()
    
    # TODO: to nie jest najlepsze rozwiązanie, ale tymczasowo usuwamy grę jeśli ktokolwiek wychodzi
    self.game = None
    self.room = []

  def _find_person_by_websocket(self, websocket):
    for person in self.people:
      if person.websocket == websocket:
        return person
    raise ValueError(f'There is no person corresponding to given websocket: {websocket}')