import pytest
import random

from rushing_turtles.model.card_stacks import CardStacks
from rushing_turtles.model.card import Card
  
def test_get_new_should_return_first_card():
  card = Card(0, 'red', 'plus')
  stacks = CardStacks([card])
  
  actual = stacks.get_new()

  assert actual == card

def test_get_recent_should_return_recent_card():
  card = Card(0, 'red', 'plus')
  stacks = CardStacks([card])

  stacks.put(stacks.get_new())
  actual = stacks.get_recent()

  assert actual == card

def test_get_new_should_raise_exception_when_no_more_cards_available():
  card = Card(0, 'red', 'plus')
  stacks = CardStacks([card])
  stacks.get_new()

  with pytest.raises(ValueError):
    stacks.get_new()

def test_get_new_should_return_first_card_when_all_cards_were_played():
  card1 = Card(0, 'red', 'plus')
  card2 = Card(1, 'green', 'minus')
  stacks = CardStacks([card1, card2])

  stacks.put(stacks.get_new())
  stacks.put(stacks.get_new())
  actual = stacks.get_new()

  assert actual == card1

def test_recent_card_should_not_change_when_all_cards_were_played():
  card1 = Card(0, 'red', 'plus')
  card2 = Card(1, 'green', 'minus')
  stacks = CardStacks([card1, card2])

  stacks.put(stacks.get_new())
  stacks.put(stacks.get_new())
  actual = stacks.get_recent()

  assert actual == card2
  
def test_get_new_should_return_reshuffled_cards_when_all_cards_were_played():
  random.seed(0)

  card1 = Card(0, 'red', 'plus')
  card2 = Card(1, 'green', 'minus')
  card3 = Card(2, 'blue', 'arrow')
  stacks = CardStacks([card1, card2, card3])

  for _ in range(3):
    stacks.put(stacks.get_new())
  
  actual = stacks.get_new()

  assert actual == card2

def test_get_new_cards_should_return_cards():
  card1 = Card(0, 'red', 'plus')
  card2 = Card(1, 'green', 'minus')
  stacks = CardStacks([card1, card2])

  actual = stacks.get_new_cards(2)

  assert actual == [card1, card2]