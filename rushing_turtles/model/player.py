from typing import List

from rushing_turtles.model.person import Person
from rushing_turtles.model.turtle import Turtle
from rushing_turtles.model.card import Card

class Player(object):
  person: Person
  turtle: Turtle
  cards: List[Card]

  def has_card(self, card : Card):
    return card in self.cards

  def has_only_backward_cards(self):
    return all([card.is_backward() for card in self.cards])  