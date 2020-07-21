
COLORS = ['RED', 'BLUE', 'GREEN', 'YELLOW', 'PURPLE', 'RAINBOW']
OFFSETS = {
  'PLUS': 1, 'PLUS_PLUS': 2, 'ARROW': 1, 'ARROW_ARROW': 2, 'MINUS': -1
}
  
class Card(object):
  id : int
  color : str
  symbol : str
  offset : int

  def __init__(self, id, color, symbol):
    if color not in COLORS:
      raise ValueError(f'Wrong card color: {color}')

    if symbol not in OFFSETS.keys():
      raise ValueError(f'Wrong card symbol: {symbol}')
    
    if symbol in ['ARROW', 'ARROW_ARROW'] and color != 'RAINBOW':
      raise ValueError('Only rainbow cards can have arrows symbol')

    self.id = id
    self.color = color
    self.symbol = symbol
    self.offset = OFFSETS[symbol]
  
  def is_rainbow(self):
    return self.color == 'RAINBOW'

  def __eq__(self, other):
    return self.id == other.id

  def __hash__(self):
    return hash(self.id)

  def __repr__(self):
    return f'Card(id={self.id}, color={self.color}, symbol={self.symbol})'
    