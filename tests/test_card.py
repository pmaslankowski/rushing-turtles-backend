import pytest

from rushing_turtles.model.card import Card

def test_should_raise_when_color_is_not_valid():
  with pytest.raises(ValueError):
    Card(0, 'red', 'wrong symbol')

def test_should_raise_when_symbol_is_not_valid():
  with pytest.raises(ValueError):
    Card(0, 'RED', 'wrong symbol')

def test_should_raise_when_not_rainbow_card_has_arrow_symbol():
  with pytest.raises(ValueError):
    Card(0, 'RED', 'ARROW')
  
def test_should_raise_when_not_rainbow_card_has_double_arrow_symbol():
  with pytest.raises(ValueError):
    Card(0, 'RED', 'ARROW_ARROW')

offsets = [
  ('PLUS', 1),
  ('PLUS_PLUS', 2),
  ('ARROW', 1), 
  ('ARROW_ARROW', 2),
  ('MINUS', -1)
]
@pytest.mark.parametrize('symbol, expected', offsets)
def test_offset_should_return_corresponding_offset(symbol, expected):
  card = Card(0, 'RAINBOW', symbol)
  
  actual = card.offset

  assert actual == expected

def test_is_rainbow_should_return_true_for_rainbow_card():
  card = Card(0, 'RAINBOW', 'PLUS')

  assert card.is_rainbow()

def test_is_rainbow_should_return_false_for_regular_card():
  card = Card(0, 'RED', 'PLUS')

  assert card.is_rainbow() == False