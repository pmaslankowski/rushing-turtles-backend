import pytest

from rushing_turtles.model.action import Action
from rushing_turtles.model.card import Card

def test_get_color_should_return_card_color():
  action = Action(Card(0, 'RED', 'PLUS'))

  actual = action.get_color()

  assert actual == 'red'