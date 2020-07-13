import pytest

from rushing_turtles.model.card import Card

def test_should_raise_when_symbol_is_not_valid():
  with pytest.raises(ValueError):
    Card(0, 'red', 'wrong symbol')

offsets = [
  ('PLUS', 1),
  ('PLUS_PLUS', 2),
  ('ARROW', 1), 
  ('ARROW_ARROW', 2),
  ('MINUS', -1)
]
@pytest.mark.parametrize('symbol, expected', offsets)
def test_offset_should_return_corresponding_offset(symbol, expected):
  card = Card(0, 'red', symbol)
  
  actual = card.offset

  assert actual == expected