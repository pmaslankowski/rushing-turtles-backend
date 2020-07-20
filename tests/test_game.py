import random
import pytest

from rushing_turtles.model.game import Game, HAND_SIZE, create_game
from rushing_turtles.model.player import Player
from rushing_turtles.model.board import Board
from rushing_turtles.model.turtle import Turtle
from rushing_turtles.model.card_stacks import CardStacks
from rushing_turtles.model.card import Card
from rushing_turtles.model.person import Person
from rushing_turtles.model.action import Action

@pytest.fixture(autouse=True)
def init_rand_seed():
  random.seed(0)

def test_game_with_no_players_should_fail():
  with pytest.raises(ValueError):
    Game([], [], [])

def test_game_with_one_player_shoud_fail():
  with pytest.raises(ValueError):
    Game([Person(0, 'Piotr')], [], [])

def test_game_without_cards_should_fail():
  with pytest.raises(ValueError):
    Game(
      [Person(0, 'Piotr'), Person(1, 'Marta')], 
      [Turtle('GREEN'), Turtle('RED')],
      [])

def test_game_with_not_enough_cards_should_fail():
  with pytest.raises(ValueError):
    Game(
      [Person(0, 'Piotr'), Person(1, 'Marta')], 
      [Turtle('GREEN'), Turtle('RED')],
      [Card(0, 'RED', 'PLUS') for _ in range(2*HAND_SIZE-1)])

def test_players_should_correspond_to_people():
  people = [Person(0, 'Piotr'), Person(1, 'Marta')]
  game = Game(
    people,
    [Turtle('GREEN'), Turtle('RED')],
    [Card(0, 'RED', 'PLUS') for _ in range(2*HAND_SIZE)])

  assert [player.person for player in game.players] == people

def test_first_person_should_become_first_player():
  people = [Person(0, 'Piotr'), Person(1, 'Marta')]

  game = Game(
    people,
    [Turtle('GREEN'), Turtle('RED')],
    [Card(0, 'RED', 'PLUS') for _ in range(2*HAND_SIZE)])
  
  assert game.active_player.person == people[0]

def test_first_player_should_get_another_hand_when_he_cant_move(people, turtles):
  cards = [Card(i, 'RED', 'MINUS') for i in range(HAND_SIZE)]
  cards += [Card(i, 'GREEN', 'PLUS') for i in range(HAND_SIZE, 3*HAND_SIZE)]
  
  game = Game(people, turtles, cards)
  
  assert game.players[0].cards == cards[2*HAND_SIZE:3*HAND_SIZE]

def test_player_should_keep_getting_another_hand_until_he_can_move(people, turtles):
  cards = [Card(i, 'RED', 'MINUS') for i in range(HAND_SIZE)]
  cards += [Card(i, 'RAINBOW', 'MINUS') for i in range(HAND_SIZE, 2*HAND_SIZE)]
  cards += [Card(i, 'GREEN', 'PLUS') for i in range(2*HAND_SIZE, 4*HAND_SIZE)]
  
  game = Game(people, turtles, cards)
  
  assert game.players[0].cards == cards[2*HAND_SIZE:3*HAND_SIZE]

def test_should_raise_exception_when_other_player_tries_to_move(cards, game):
  other = Person(123, 'Unknown')

  with pytest.raises(ValueError):
    game.play(other, Action(Card(0, 'RED', 'ARROW')))

def test_should_raise_when_inactive_player_tries_to_move(cards, people, game):
  inactive_player = people[1]

  with pytest.raises(ValueError):
    game.play(inactive_player, Action(Card(0, 'RED', 'ARROW')))

def test_should_raise_when_player_doesnt_have_given_card(cards, people, game):
  player = people[0]

  with pytest.raises(ValueError):
    game.play(player, Action(Card(42, 'RED', 'ARROW')))

def test_should_raise_when_turtle_with_given_color_doesnt_exist(cards, people, game):
  player = people[0]
  
  with pytest.raises(ValueError):
    game.play(player, Action(Card(0, 'BLUE', 'PLUS')))
  
def test_corresponding_turtle_should_move(cards, people, game):
  player = people[0]
  
  game.play(player, Action(Card(0, 'RED', 'PLUS')))
  
  assert game.board.further_fields[0] == [Turtle('RED')]

def test_card_played_by_player_should_be_recent_on_stack(cards, people, game):
  player = game.players[0]
  card = Card(0, 'RED', 'PLUS')
  
  game.play(player.person, Action(card))

  assert game.stacks.get_recent() == card

def test_player_should_not_have_played_card_after_move(cards, people, game):
  player = game.players[0]
  card = Card(0, 'RED', 'PLUS')

  game.play(player.person, Action(card))

  assert card not in player.cards

def test_player_should_get_new_card_after_move(game, cards):
  player = game.players[0]

  game.play(player.person, Action(Card(0, 'RED', 'PLUS')))

  next_card_from_stack = cards[2*HAND_SIZE]
  assert len(player.cards) == HAND_SIZE
  assert player.cards[0] == next_card_from_stack

def test_next_player_should_become_active_after_move(game):
  player = game.players[0]

  game.play(player.person, Action(Card(0, 'RED', 'PLUS')))

  assert game.active_player == game.players[1]

def test_first_player_should_be_active_after_two_moves(game):
  first_player = game.players[0]
  second_player = game.players[1]

  game.play(first_player.person, Action(Card(0, 'RED', 'PLUS')))
  game.play(second_player.person, Action(Card(5, 'RED', 'PLUS')))

  assert game.active_player == first_player

def test_third_player_should_be_active_after_two_moves(cards):
  people = [Person(0, 'Piotr'), Person(1, 'Marta'), Person(2, 'Ewa')]
  turtles = [Turtle('GREEN'), Turtle('RED'), Turtle('BLUE')]
  game = Game(people, turtles, cards)

  game.play(people[0], Action(Card(0, 'RED', 'PLUS')))
  game.play(people[1], Action(Card(5, 'RED', 'PLUS')))
  game.play(people[2], Action(Card(10, 'RED', 'PLUS')))

  assert game.active_player == game.players[0]

def test_first_player_should_be_active_after_three_moves(cards):
  people = [Person(0, 'Piotr'), Person(1, 'Marta'), Person(2, 'Ewa')]
  turtles = [Turtle('GREEN'), Turtle('RED'), Turtle('BLUE')]
  game = Game(people, turtles, cards)

  game.play(people[0], Action(Card(0, 'RED', 'PLUS')))
  game.play(people[1], Action(Card(5, 'RED', 'PLUS')))

  assert game.active_player == game.players[2]

def test_next_player_should_get_new_hand_if_he_cant_move(people, turtles):
  # Initial state:
  # First player cards: 0,1,2,3,4
  # Second player cards: 5,6,7,8,9
  #
  # First player plays 0 and takes next card (10)
  # Second player can't make any move, so he should take another hand:
  # 11, 12, 13, 14, 15

  cards = [Card(i, 'GREEN', 'PLUS') for i in range(HAND_SIZE)]
  cards += [Card(i, 'RED', 'MINUS') for i in range(HAND_SIZE, 2*HAND_SIZE)]
  cards += [Card(i, 'GREEN', 'PLUS') for i in range(2*HAND_SIZE, 4*HAND_SIZE)]
  
  game = Game(people, turtles, cards)
  player = game.players[0]

  game.play(player.person, Action(Card(0, 'GREEN', 'PLUS')))

  assert game.players[1].cards == cards[2*HAND_SIZE+1:3*HAND_SIZE+1]

def test_next_player_should_keep_getting_hands_until_he_can_move(people, turtles):
  # Initial state:
  # First player cards: 0,1,2,3,4
  # Second player cards: 5,6,7,8,9
  #
  # First player plays 0 and takes next card (10)
  # Second player can't make any move, so he should take another hand:
  # 11, 12, 13, 14, 15
  # He still can't make any move so he takes another hand:
  # 16, 17, 18, 19, 20

  cards = [Card(i, 'GREEN', 'PLUS') for i in range(HAND_SIZE)]
  cards += [Card(i, 'RED', 'MINUS') for i in range(HAND_SIZE, 3*HAND_SIZE+1)]
  cards += [Card(i, 'GREEN', 'PLUS') for i in range(3*HAND_SIZE, 4*HAND_SIZE+1)]
  
  game = Game(people, turtles, cards)
  player = game.players[0]

  game.play(player.person, Action(Card(0, 'GREEN', 'PLUS')))

  assert game.players[1].cards == cards[3*HAND_SIZE+1:4*HAND_SIZE+1]

def test_play_should_return_winner_when_player_wins(game, people):
  for _ in range(8):
    active = game.active_player
    game.play(active.person, Action(active.cards[0]))
  
  active = game.active_player
  winner = game.play(active.person, Action(active.cards[0]))  

  assert winner == people[1]

def test_play_should_return_none_when_there_is_no_winner_yet(game, people):
  player = people[0]
  
  winner = game.play(player, Action(Card(0, 'RED', 'PLUS')))
  
  assert winner == None

def test_get_person_idx_should_return_idx(game, people):
  person = people[0]

  actual = game.get_person_idx(person)

  assert actual == 0

def test_get_person_idx_should_raise_when_person_is_not_in_game(game, people):
  person = Person(2, 'Other')

  with pytest.raises(ValueError):
    game.get_person_idx(person)

def test_get_card_should_raise_when_card_not_exists_in_the_game(game):
  with pytest.raises(ValueError):
    game.get_card(42)

def test_get_card_should_return_card_with_given_id(game):
  actual = game.get_card(0)

  assert actual == Card(0, 'RED', 'PLUS')

def test_get_persons_cards_should_raise_when_person_is_not_a_player(game):
  with pytest.raises(ValueError):
    game.get_persons_cards(Person(2, 'Other'))

def test_get_persons_cards_should_return_cards(game):
  cards = game.get_persons_cards(Person(0, 'Piotr'))

  assert cards == game.players[0].cards

def test_create_game_should_create_game(people):
  game = create_game(people)

  assert len(game.players) == len(people)
  assert len(game.turtles) == 5
  assert len(game.stacks.available_cards) == 42

@pytest.fixture
def people():
  return [Person(0, 'Piotr'), Person(1, 'Marta')]

@pytest.fixture
def turtles():
  return [Turtle('GREEN'), Turtle('RED')]

@pytest.fixture
def cards():
  return [Card(i, 'RED', 'PLUS') for i in range(4*HAND_SIZE)]

@pytest.fixture
def game(people, turtles, cards):
  return Game(people, turtles, cards)