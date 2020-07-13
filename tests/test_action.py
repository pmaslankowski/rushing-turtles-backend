import pytest

from rushing_turtles.model.action import Action
from rushing_turtles.model.card import Card

def test_get_color_should_return_card_color_when_action_color_is_not_set():
  action = Action(Card(0, 'RED', 'PLUS'))

  actual = action.get_color()

  assert actual == 'RED'

def test_should_raise_when_action_color_is_present_and_card_is_not_rainbow():
  with pytest.raises(ValueError):
    Action(Card(0, 'RED', 'PLUS'), 'RED')
      
def test_get_color_should_return_action_color_when_it_is_present():
  action = Action(Card(0, 'RAINBOW', 'PLUS'), 'RED')

  actual = action.get_color()

  assert actual == 'RED'

