
class Turtle(object):
  color : str

  def __init__(self, color):
    self.color = color

  def __str__(self):
    return self.color
  
  def __repr__(self):
    return self.color