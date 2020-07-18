import pytest
import json
import asyncio

from unittest.mock import Mock
from rushing_turtles.server import GameController
from rushing_turtles.messages import MsgToSend, HelloServerMsg
from rushing_turtles.model.person import Person

def test_should_emit_can_create_when_first_player_joins():
  controller = GameController()
  
  actual = controller.handle(HelloServerMsg(0, 'Piotr'), 0)

  expected = MsgToSend(0, 
    message='hello client', 
    status='can create', 
    list_of_players_in_room=[])
  
  assert actual == expected

def test_should_emit_can_join_when_another_player_joins():
  controller = GameController()

  controller.handle(HelloServerMsg(0, 'Piotr'), 0)

  actual = controller.handle(HelloServerMsg(1, 'Marta'), 1)

  expected = MsgToSend(1,
    message='hello client',
    status='can join',
    list_of_players_in_room=['Piotr'])

  #assert actual == expected