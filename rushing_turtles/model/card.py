
class Card(object):
  id : int
  color : str
  action : str

  def __init__(self, id, color, action):
    self.id = id
    self.color = color
    self.action = action
