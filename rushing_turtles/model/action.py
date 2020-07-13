from rushing_turtles.model.card import Card

class Action(object):
  card: Card
  color : str
  
  def __init__(self, card : Card, color=None):
    self.card = card
    self.color = color
  
  def get_offset(self):
    return self.card.offset

  def get_color(self):
    if 