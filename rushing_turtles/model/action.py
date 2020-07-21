from rushing_turtles.model.card import Card

class Action(object):
  card: Card
  color : str
  
  def __init__(self, card : Card, color=None):
    if color and not card.is_rainbow():
      raise ValueError(
        f'Action color can be set on actions concerning rainbow cards only.' 
        +' Card color: {card.color}')
    if not color and card.is_rainbow():
      raise ValueError('Action color must be set on actions concerning rainbow cards')

    self.card = card
    self.color = color
  
  def get_offset(self):
    return self.card.offset

  def get_color(self):
    return self.color if self.card.is_rainbow() else self.card.color

  def does_move_last_turtle(self):
    return self.card.symbol in ['ARROW', 'ARROW_ARROW']