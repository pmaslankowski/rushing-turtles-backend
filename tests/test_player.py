import pytest

from rushing_turtles.model.person import Person
from rushing_turtles.model.player import Player
from rushing_turtles.model.turtle import Turtle
from rushing_turtles.model.card import Card

def test_has_card_should_return_false_when_user_has_no_cards(person, turtle):
  cards = []
  player = Player(person, turtle, cards)

  actual = player.has_card(Card(0, 'RED', 'PLUS'))

  assert not actual

def test_has_card_should_return_false_when_user_has_other_card(person, turtle):
  cards = [Card(1, 'RED', 'MINUS')]
  player = Player(person, turtle, cards)

  actual = player.has_card(Card(0, 'RED', 'PLUS'))

  assert not actual

def test_has_card_should_return_true_when_user_has_given_card(person, turtle):
  card = Card(0, 'RED', 'PLUS')
  player = Player(person, turtle, [card])

  actual = player.has_card(card)

  assert actual

def test_has_card_should_return_true_when_user_has_given_card_in_two_cards(person, turtle):
  cards = [Card(0, 'RED', 'PLUS'), Card(1, 'RED', 'MINUS')]
  player = Player(person, turtle, cards)

  actual = player.has_card(cards[0])

  assert actual

def test_add_card_should_add_card_for_player_with_no_cards(person, turtle):
  card = Card(0, 'RED', 'PLUS')
  player = Player(person, turtle, [])
  
  player.add_card(card)

  assert player.has_card(card)

def test_add_card_should_add_card_for_player_with_one_card(person, turtle):
  player = Player(person, turtle, [Card(0, 'RED', 'PLUS')])
  card = Card(1, 'RED', 'MINUS')

  player.add_card(card)

  assert player.has_card(card)

def test_new_card_should_be_the_first_of_player_cards(person, turtle):
  player = Player(person, turtle, [Card(0, 'RED', 'PLUS')])
  card = Card(1, 'RED', 'MINUS')

  player.add_card(card)

  assert player.cards[0] == card

def test_new_card_should_add_card_for_player_with_two_cards(person, turtle):
  cards = [Card(0, 'RED', 'PLUS'), Card(1, 'GREEN', 'MINUS')]
  player = Player(person, turtle, cards)
  card = Card(2, 'RAINBOW', 'ARROW')

  player.add_card(card)

  assert player.cards[0] == card

def test_remove_card_should_raise_when_player_has_no_cards(person, turtle):
  player = Player(person, turtle, [])
  
  with pytest.raises(ValueError):
    player.remove_card(Card(0, 'RED', 'MINUS'))

def test_remove_card_should_raise_when_player_has_other_card(person, turtle):
  player = Player(person, turtle, [Card(1, 'RED', 'MINUS')])

  with pytest.raises(ValueError):
    player.remove_card(Card(0, 'RED', 'PLUS'))

def test_player_should_have_no_cards_after_removal_of_his_only_card(person, turtle):
  card = Card(0, 'RED', 'PLUS')
  player = Player(person, turtle, [card])

  player.remove_card(card)

  assert not player.cards

def test_player_shouldnt_have_card_after_its_removal(person, turtle):
  card = Card(0, 'RED', 'PLUS')
  cards = [card, Card(1, 'RED', 'MINUS')]
  player = Player(person, turtle, cards)

  player.remove_card(card)

  assert not player.has_card(card)

@pytest.fixture
def person():
  return Person(0, 'Piotr')

@pytest.fixture
def turtle():
  return Turtle('RED')