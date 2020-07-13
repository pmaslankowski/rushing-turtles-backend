from typing import List

from rushing_turtles.model.person import Person
from rushing_turtles.model.turtle import Turtle
from rushing_turtles.model.card import Card

class Player(object):
  person: Person
  turtle: Turtle
  cards: List[Card]

  def __init__(self, person : Person, turtle : Turtle, cards : List[Card]):
    self.person = person
    self.turtle = turtle
    self.cards = cards

  def has_card(self, card : Card):
    return card in self.cards

  def has_only_backward_cards(self):
    return all([card.is_backward() for card in self.cards])  