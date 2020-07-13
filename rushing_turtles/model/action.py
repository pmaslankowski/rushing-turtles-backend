from rushing_turtles.model.card import Card

class Action(object):
  card: Card
  
  def __init__(self, card : Card):
    self.card = card

  def get_offset(self):
    return self.card.offset

  def get_color(self):
    return self.card.color