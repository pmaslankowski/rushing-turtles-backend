import random

from typing import List

from rushing_turtles.model.card import Card
from rushing_turtles.model.player import Player
from rushing_turtles.model.board import Board
from rushing_turtles.model.action import Action
from rushing_turtles.model.card_stacks import CardStacks

HAND_SIZE = 5

class Game(object):
  stacks: CardStacks
  board : Board
  players: List[Player]
  active_player: Player

  def __init__(self, board, stacks, players):
    if len(players) < 2:
      raise ValueError('Game requires at least 2 players')

    self.stacks = stacks
    self.players = players
    self.board = board
    self.active_player = players[0]

    
  def play(self, player : Player, action : Action) -> None:
    if not player == self.active_player:
      raise ValueError(f'Player {player} is not an active player right now')

    played_card = action.get_played_card()

    if played_card not in player.cards:
      raise ValueError("Player doesn't have the card in the hand")

    self.reject_card(player, played_card)

    self.board.move(action.get_turtle(), action.get_move())

    player.cards.append(self.stacks.get_new())

    if player.has_only_backward_cards():
      self.cards = self.stacks.get_cards(HAND_SIZE)

    self.next_turn()

  def next_turn(self) -> None:
    active_idx = self.players.index(self.active_player)
    next_idx = (active_idx + 1) % len(self.players)
    self.active_player = self.players[next_idx]

  def reject_card(self, player : Player, card : Card) -> None:
    player.cards.remove(card)
    self.stacks.put(card)