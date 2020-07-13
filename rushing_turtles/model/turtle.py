
COLORS = ['RED', 'BLUE', 'GREEN', 'YELLOW', 'PURPLE']

class Turtle(object):
  color : str

  def __init__(self, color):
    if color not in COLORS:
      raise ValueError(f'Invalid color: {color}')
    self.color = color

  def __eq__(self, other):
    return self.color == other.color

  def __hash__(self):
    return hash(self.color)
    
  def __repr__(self):
    return self.color