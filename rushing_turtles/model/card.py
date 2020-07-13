
OFFSETS = {
  'PLUS': 1, 'PLUS_PLUS': 2, 'ARROW': 1, 'ARROW_ARROW': 2, 'MINUS': -1
}
  
class Card(object):
  id : int
  color : str
  symbol : str
  offset : int

  def __init__(self, id, color, symbol):
    if symbol not in OFFSETS.keys():
      raise ValueError(f'Wrong symbol: {symbol}')

    self.id = id
    self.color = color
    self.symbol = symbol
    self.offset = OFFSETS[symbol]
  
  def __eq__(self, other):
    return self.id == other.id

  def __hash__(self):
    return hash(self.id)

  def __repr__(self):
    return f'Card(color={self.color}, symbol={self.symbol})'