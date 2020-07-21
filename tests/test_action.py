import pytest

from rushing_turtles.model.action import Action
from rushing_turtles.model.card import Card

def test_init_should_raise_when_color_is_set_on_regular_card():
  with pytest.raises(ValueError):
    Action(Card(0, 'RED', 'PLUS'), 'BLUE')

def test_init_should_raise_when_color_is_not_set_on_rainbow_card():
  with pytest.raises(ValueError):
    Action(Card(0, 'RAINBOW', 'PLUS'))

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

def test_does_move_last_turtle_should_return_true_when_card_symbol_is_arrow():
  action = Action(Card(0, 'RAINBOW', 'ARROW'), 'RED')

  actual = action.does_move_last_turtle()

  assert actual
  
def test_does_move_last_turtle_should_return_true_when_card_symbol_is_double_arrow():
  action = Action(Card(0, 'RAINBOW', 'ARROW_ARROW'), 'RED')

  actual = action.does_move_last_turtle()

  assert actual  

def test_does_move_last_turtle_should_return_false_when_card_symbol_is_plus():
  action = Action(Card(0, 'RAINBOW', 'PLUS'), 'RED')

  actual = action.does_move_last_turtle()

  assert not actual  
