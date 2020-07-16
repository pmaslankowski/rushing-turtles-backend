import random

from typing import List

from rushing_turtles.model.card import Card
from rushing_turtles.model.player import Player
from rushing_turtles.model.board import Board
from rushing_turtles.model.action import Action
from rushing_turtles.model.card_stacks import CardStacks
from rushing_turtles.model.person import Person
from rushing_turtles.model.turtle import Turtle

HAND_SIZE = 5

class Game(object):
  stacks: CardStacks
  turtles : List[Turtle]
  board : Board
  players: List[Player]
  active_player: Player

  def __init__(self, people : List[Person], turtles : List[Turtle], cards : List[Card]):
    if len(people) < 2:
      raise ValueError('There are at least 2 players required to start the game')
    if len(turtles) < len(people):
      raise ValueError('Numbers of players and turtles should be equal')
    if len(cards) < HAND_SIZE * len(people):
      raise ValueError(f'Not enough cards for {len(people)} players')

    self.stacks = CardStacks(cards)
    self.turtles = turtles
    self.board = Board(turtles)
    self.players = self._init_players(people, turtles)
    self.active_player = self.players[0]

    self._ensure_player_can_move(self.active_player)

  def _init_players(self, people : List[Person], turtles : List[Turtle]):
    random.shuffle(turtles)
    return [self._init_player(person, turtle) for person, turtle in zip(people, turtles)]

  def _init_player(self, person : Person, turtle : Turtle):
    return Player(person, turtle, self.stacks.get_new_cards(HAND_SIZE))

  def _ensure_player_can_move(self, player : Player):
    while not self._can_player_move(player):
      player.cards = self.stacks.get_new_cards(HAND_SIZE)

  def _can_player_move(self, player : Player):
    return any([self.board.is_move_with_card_possible(card) 
                  for card in player.cards])
  
  def play(self, person : Person, action : Action) -> None:
      player = self._find_player(person)
      if player != self.active_player:
        raise ValueError(f"It is not {person}'s turn yet")
      if not player.has_card(action.card):
        raise ValueError(f"Player doesn't have given card")
      
      self._move_turtle(action)
      self._update_player_cards_and_stacks(player, action)

      if self._has_winner():
        return self._get_winner()
      
      self._change_active_player()
      self._ensure_player_can_move(self.active_player)

  def _find_player(self, person : Person):
    for player in self.players:
      if player.person == person:
        return player
    raise ValueError(f'Person {person} does not play in this game')  
  
  def _move_turtle(self, action : Action):
    turtle = self._find_turtle(action.get_color())
    self.board.move(turtle, action.get_offset())
  
  def _find_turtle(self, color : str):
    for turtle in self.turtles:
      if turtle.color == color:
        return turtle
    raise ValueError(f'{color} turtle doesnt exist in this game')
  
  def _update_player_cards_and_stacks(self, player : Player, action : Action):
    self.stacks.put(action.card)
    player.remove_card(action.card)
    new_card = self.stacks.get_new()
    player.add_card(new_card)
  
  def _has_winner(self):
    return self.board.has_anyone_finished()
    
  def _get_winner(self):
    winning_turtle = self.board.get_top_last_turtle()
    winner = self._find_player_by_turtle(winning_turtle)
    return winner.person

  def _find_player_by_turtle(self, turtle : Turtle):
    for player in self.players:
      if player.turtle == turtle:
        return player
    raise ValueError(f'No player with given turtle: {turtle}')

  def _change_active_player(self):
    active_player_idx = self._find_player_idx(self.active_player)
    next_idx = (active_player_idx + 1) % len(self.players)
    self.active_player = self.players[next_idx]
  
  def _find_player_idx(self, player : Player):
    for idx, current in enumerate(self.players):
      if current == player:
        return idx
    raise ValueError(f'Player {player} does not play in this game')