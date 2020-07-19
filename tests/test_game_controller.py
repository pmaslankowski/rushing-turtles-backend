import pytest
import json
import asyncio

from unittest.mock import Mock

from rushing_turtles.game_controller import GameController, MAX_PLAYERS_IN_ROOM
from rushing_turtles.messages import MsgToSend
from rushing_turtles.messages import HelloServerMsg
from rushing_turtles.messages import WantToJoinMsg
from rushing_turtles.messages import StartGameMsg
from rushing_turtles.model.person import Person

def test_should_emit_can_create_when_first_player_joins():
  controller = GameController()
  
  actual = controller.handle(HelloServerMsg(0, 'Piotr'), 0)

  expected = MsgToSend(0, 
    message='hello client', 
    status='can create', 
    list_of_players_in_room=[])
  
  assert actual == expected

def test_should_raise_when_player_with_given_id_is_already_connected():
  controller = GameController()

  controller.handle(HelloServerMsg(0, 'Piotr'), 0)

  with pytest.raises(ValueError):
    controller.handle(HelloServerMsg(0, 'Piotr'), 0)

def test_should_raise_when_player_tries_to_create_room_but_is_not_in_lounge():
  controller = GameController()

  with pytest.raises(ValueError):
    controller.handle(WantToJoinMsg('create the game', 0), 0)

def test_should_raise_when_player_tries_to_create_game_but_its_already_created():
  controller = GameController()

  controller.handle(HelloServerMsg(0, 'Piotr'), 0)
  controller.handle(WantToJoinMsg('create the game', 0), 0)
  controller.handle(HelloServerMsg(1, 'Marta'), 1)
  
  with pytest.raises(ValueError):
    controller.handle(WantToJoinMsg('create the game', 1), 1)

def test_should_emit_room_updated_when_player_creates_the_room():
  controller = GameController()

  controller.handle(HelloServerMsg(0, 'Piotr'), 0)
  actual = controller.handle(WantToJoinMsg('create the game', 0), 0)
  expected_msg = MsgToSend(0,
    message='room update',
    list_of_players_in_room=['Piotr'])

  assert expected_msg in actual

def test_should_broadcast_room_updated_when_player_creates_the_room():
  controller = GameController()

  controller.handle(HelloServerMsg(0, 'Piotr'), 0)
  controller.handle(HelloServerMsg(1, 'Marta'), 1)
  actual = controller.handle(WantToJoinMsg('create the game', 0), 0)

  expected_msgs = [
    MsgToSend(0, 
      message='room update', 
      list_of_players_in_room=['Piotr']),
    MsgToSend(1,
      message='room update',
      list_of_players_in_room=['Piotr'])
  ]

  for msg in expected_msgs:
    assert msg in actual

def test_should_emit_can_join_when_another_player_connects():
  controller = GameController()

  controller.handle(HelloServerMsg(0, 'Piotr'), 0)
  controller.handle(WantToJoinMsg('create the game', 0), 0)

  actual = controller.handle(HelloServerMsg(1, 'Marta'), 1)

  expected = MsgToSend(1,
    message='hello client',
    status='can join',
    list_of_players_in_room=['Piotr'])

  assert actual == expected

def test_should_raise_when_player_wants_to_join_the_room_but_room_doesnt_exist():
  controller = GameController()

  controller.handle(HelloServerMsg(0, 'Piotr'), 0)
  with pytest.raises(ValueError):
    controller.handle(WantToJoinMsg('join the game', 0), 0)

def test_should_raise_when_player_wants_to_join_the_room_but_is_not_connected():
  controller = GameController()
  
  with pytest.raises(ValueError):
   controller.handle(WantToJoinMsg('join the game', 0), 0)

def test_should_raise_when_player_wants_to_join_room_that_they_are_already_in():
  controller = GameController()

  controller.handle(HelloServerMsg(0, 'Piotr'), 0)
  controller.handle(WantToJoinMsg('create the game', 0), 0)

  with pytest.raises(ValueError):
    controller.handle(WantToJoinMsg('join the game', 0), 0)

def test_should_broadcast_room_update_when_another_player_joins_the_room():
  controller = GameController()

  controller.handle(HelloServerMsg(0, 'Piotr'), 0)
  controller.handle(HelloServerMsg(1, 'Marta'), 1)
  controller.handle(WantToJoinMsg('create the game', 0), 0)
  actual = controller.handle(WantToJoinMsg('join the game', 1), 1)

  expected = [
    MsgToSend(0, message='room update', list_of_players_in_room=['Piotr', 'Marta']),
    MsgToSend(1, message='room update', list_of_players_in_room=['Piotr', 'Marta'])
  ]

  for msg in expected:
    assert msg in actual 

def test_should_broadcast_room_update_to_all_players_except_the_one_that_joined_room():
  controller = GameController()

  controller.handle(HelloServerMsg(0, 'Piotr'), 0)
  controller.handle(HelloServerMsg(1, 'Marta'), 1)

  actual = controller.handle(WantToJoinMsg('create the game', 0), 0)

  expected = MsgToSend(1,
    message='hello client', 
    status='can join', 
    list_of_players_in_room=['Piotr'])

  assert expected in actual

def test_shouldnt_send_can_join_msg_to_player_who_created_the_room():
  controller = GameController()

  controller.handle(HelloServerMsg(0, 'Piotr'), 0)
  controller.handle(HelloServerMsg(1, 'Marta'), 1)

  actual = controller.handle(WantToJoinMsg('create the game', 0), 0)

  not_expected = MsgToSend(0,
    message='hello client',
    status='can join',
    list_of_players_in_room=['Piotr'])

  assert not_expected not in actual

def test_should_emit_limit_on_hello_server_when_there_are_five_players_already():
  controller = GameController()

  controller.handle(HelloServerMsg(0, f'Player_0'), 0)
  controller.handle(WantToJoinMsg('create the game', 0), 0)

  for i in range(1, MAX_PLAYERS_IN_ROOM):
    controller.handle(HelloServerMsg(i, f'Player_{i}'), i)
    controller.handle(WantToJoinMsg('join the game', i), i)

  actual = controller.handle(HelloServerMsg(5, 'Player_5'), 5)

  assert actual == MsgToSend(5, 
    message='hello client',
    status='limit',
    list_of_players_in_room=[f'Player_{i}' for i in range(5)])

def test_should_raise_when_player_tries_to_join_full_room():
  controller = GameController()

  controller.handle(HelloServerMsg(0, f'Player_0'), 0)
  controller.handle(WantToJoinMsg('create the game', 0), 0)

  for i in range(1, MAX_PLAYERS_IN_ROOM):
    controller.handle(HelloServerMsg(i, f'Player_{i}'), i)
    controller.handle(WantToJoinMsg('join the game', i), i)
  
  controller.handle(HelloServerMsg(5, 'Player_5'), 5)
  with pytest.raises(ValueError):
    controller.handle(WantToJoinMsg('join the game', 5), 5)

def test_should_raise_when_player_tries_to_pose_as_somebody_else_on_join():
  controller = GameController()

  controller.handle(HelloServerMsg(0, 'Piotr'), 0)
  controller.handle(HelloServerMsg(1, 'Marta'), 1)

  with pytest.raises(ValueError):
    controller.handle(WantToJoinMsg('create the game', 1), 0)

def test_should_remove_player_from_connected_when_player_disconnects():
  controller = GameController()
  controller.handle(HelloServerMsg(0, 'Piotr'), 0)

  controller.disconnected(0)

  with pytest.raises(ValueError):
    controller.handle(WantToJoinMsg('create the game', 0), 0)

def test_should_remove_player_from_room_when_player_disconnects():
  controller = GameController()
  controller.handle(HelloServerMsg(0, 'Piotr'), 0)
  controller.handle(WantToJoinMsg('create the game', 0), 0)

  controller.disconnected(0)

  with pytest.raises(ValueError):
    controller.handle(StartGameMsg(0), 0)  

def test_should_raise_when_player_who_is_not_in_room_tries_to_start_the_game():
  controller = GameController()

  controller.handle(HelloServerMsg(0, 'Piotr'), 0)
  with pytest.raises(ValueError):
    controller.handle(StartGameMsg(0), 0)

def test_should_raise_when_not_first_player_tries_to_start_the_game():
  controller = GameController()

  controller.handle(HelloServerMsg(0, 'Piotr'), 0)
  controller.handle(HelloServerMsg(1, 'Marta'), 1)
  controller.handle(WantToJoinMsg('create the game', 0), 0)
  controller.handle(WantToJoinMsg('join the game', 1), 1)

  with pytest.raises(ValueError):
    controller.handle(StartGameMsg(1), 1)

def test_should_raise_when_player_tries_to_pose_as_somebody_else_on_start_game():
  controller = GameController()

  controller.handle(HelloServerMsg(0, 'Piotr'), 0)
  controller.handle(HelloServerMsg(1, 'Marta'), 1)
  controller.handle(WantToJoinMsg('create the game', 0), 0)
  controller.handle(WantToJoinMsg('join the game', 1), 1)

  with pytest.raises(ValueError):
    controller.handle(StartGameMsg(0), 1)

def test_should_emit_ongoing_when_new_player_connects_after_game_started():
  controller = GameController()

  controller.handle(HelloServerMsg(0, 'Piotr'), 0)
  controller.handle(HelloServerMsg(1, 'Marta'), 1)
  controller.handle(WantToJoinMsg('create the game', 0), 0)
  controller.handle(WantToJoinMsg('join the game', 1), 1)
  controller.handle(StartGameMsg(0), 0)

  actual = controller.handle(HelloServerMsg(2, 'Other'), 2)

  assert actual == MsgToSend(2,
    message='hello client',
    status='ongoing',
    list_of_players_in_room=['Piotr', 'Marta']
  )

def test_should_broadcast_ongoing_to_all_players_outside_the_room_after_game_started():
  controller = GameController()

  controller.handle(HelloServerMsg(0, 'Piotr'), 0)
  controller.handle(HelloServerMsg(1, 'Marta'), 1)
  controller.handle(HelloServerMsg(2, 'Other'), 2)
  controller.handle(WantToJoinMsg('create the game', 0), 0)
  controller.handle(WantToJoinMsg('join the game', 1), 1)
  
  actual = controller.handle(StartGameMsg(0), 0)

  expected_msg = MsgToSend(2, 
    message='hello client',
    status='ongoing',
    list_of_players_in_room=['Piotr', 'Marta'])
  
  assert expected_msg in actual

def test_should_broadcast_game_ready_to_start_to_all_players_in_the_room_after_game_started():
  controller = GameController()

  controller.handle(HelloServerMsg(0, 'Piotr'), 0)
  controller.handle(HelloServerMsg(1, 'Marta'), 1)
  controller.handle(WantToJoinMsg('create the game', 0), 0)
  controller.handle(WantToJoinMsg('join the game', 1), 1)

  actual = controller.handle(StartGameMsg(0), 0)


  expected = [
    MsgToSend(0, message='game ready to start', player_idx=0),
    MsgToSend(1, message='game ready to start', player_idx=1)
  ]

  for msg in expected:
    assert msg in actual

