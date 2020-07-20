import random

from typing import List, Deque
from collections import deque

from rushing_turtles.model.card import Card

class CardStacks(object):
  played_cards: Deque[Card]
  available_cards: Deque[Card]

  def __init__(self, available_cards : List[Card]):
    self.available_cards = deque(available_cards)
    self.played_cards = deque()

  def put(self, card : Card) -> None:
    self.played_cards.appendleft(card)
  
  def get_recent(self) -> Card:
    if not self.played_cards:
      return None
    return self.played_cards[0]

  def get_new(self) -> Card:
    return self.get_new_cards(1)[0]

  def get_new_cards(self, cnt : int) -> List[Card]:
    if not self._has_enough_available_cards(cnt):
      self._reshuffle()

    if not self._has_enough_available_cards(cnt):
      raise ValueError(f'Too many cards requested ({cnt}).'
          + f'There are only {len(self.available_cards)} cards available.')

    return [self.available_cards.popleft() for _ in range(cnt)]

  def _has_enough_available_cards(self, cnt):
    return len(self.available_cards) >= cnt

  def _reshuffle(self) -> None:
    if self.played_cards:
      recently_played_card = self.played_cards.popleft()
      self.available_cards = self._shuffle_cards(self.played_cards)
      self.played_cards = deque([recently_played_card])
  
  def _shuffle_cards(self, cards : Deque[Card]) -> Deque[Card]:
    cards_list = list(cards)
    random.shuffle(cards_list)
    return deque(cards_list)