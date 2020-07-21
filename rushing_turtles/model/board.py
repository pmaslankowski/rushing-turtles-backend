from typing import List, Dict

from rushing_turtles.model.turtle import Turtle
from rushing_turtles.model.card import Card

NUMBER_OF_FIELDS = 10

class Board(object):
  start_field: List[List[Turtle]]
  further_fields: List[List[Turtle]]
  turtles : List[Turtle]

  def __init__(self, turtles):
    assert NUMBER_OF_FIELDS >= 2
    self.turtles = turtles
    self.start_field = [[turtle] for turtle in turtles]
    self.further_fields = [[] for _ in range(NUMBER_OF_FIELDS-1)]

  def is_last(self, turtle: Turtle) -> bool:
    if self._is_in_start_field(turtle):
      return True

    if self.start_field:
      return False
    
    for stack in self.further_fields:
      if stack:
        return turtle in stack 

  def has_anyone_finished(self):
    return bool(self.further_fields[-1])
  
  def get_ranking(self):
    return sorted(self.turtles, 
      key=lambda x: (self._find_pos(x), self._find_height(x), x.color), 
      reverse=True)

  def _find_height(self, turtle : Turtle):
    stack = self._find_stack(turtle)
    return len(stack) - 1 - stack.index(turtle)

  def _find_stack(self, turtle : Turtle):
    pos = self._find_pos(turtle)
    if pos > 0:
      pos_in_further_fields = pos - 1
      return self.further_fields[pos_in_further_fields]
    else:
      return self._find_stack_in_start(turtle)[1]
      
  def move(self, turtle: Turtle, offset: int) -> None:
    pos = self._find_pos(turtle)
    if pos + offset >= NUMBER_OF_FIELDS:
      raise ValueError(f"Turtle {turtle} tries to go out of the board")
  
    if pos == 0:
      self._move_from_start(turtle, offset)
    else:
      self._move_from_further_fields(turtle, pos, offset)

  def _find_pos(self, turtle: Turtle) -> int:
    if self._is_in_start_field(turtle):
      return 0
    else:
      return self._find_pos_in_further_fields(turtle)

  def _is_in_start_field(self, turtle: Turtle) -> bool:
    return any([turtle in stack for stack in self.start_field])
  
  def _find_pos_in_further_fields(self, turtle: Turtle) -> List[Turtle]:
    for idx_in_further_fields, stack in enumerate(self.further_fields):
      if turtle in stack:
        pos = idx_in_further_fields + 1
        return pos
    
    raise ValueError(f'Turtle {turtle} does not exist in further fields')
  
  def _move_from_start(self, turtle: Turtle, offset: int) -> None:
    if offset < 0:
      raise ValueError(f"Turtle can't move backward when it is in the start field")

    idx, stack = self._find_stack_in_start(turtle)
    top_part, bottom_part = self._split_stack_on_turtle(stack, turtle)
    self.further_fields[offset-1] = top_part + self.further_fields[offset-1]
    if bottom_part:    
      self.start_field[idx] = bottom_part
    else:
      self.start_field.remove(stack)

  def _find_stack_in_start(self, turtle: Turtle) -> List[Turtle]:
    for idx, stack in enumerate(self.start_field):
      if turtle in stack:
        return idx, stack
    
    raise ValueError(f'Turtle {turtle} is not in the start field')

  def _move_from_further_fields(self, turtle: Turtle, pos: int, offset: int) -> None:
    pos_in_further_fields = pos - 1
    stack = self.further_fields[pos_in_further_fields]
    top_part, bottom_part = self._split_stack_on_turtle(stack, turtle)
    
    new_pos = pos_in_further_fields + offset
    self.further_fields[pos_in_further_fields] = bottom_part

    if new_pos >= 0:
      self.further_fields[new_pos] = top_part + self.further_fields[new_pos]
    else:
      self.start_field.append(top_part)
  
  def _split_stack_on_turtle(self, stack: List[Turtle], turtle: int):
    split_idx = stack.index(turtle)
    top_part = stack[:split_idx+1]
    bottom_part = stack[split_idx+1:]
    return top_part, bottom_part
  
  def is_move_with_card_possible(self, card : Card):
    if not self.turtles:
      return False
    
    if card.is_rainbow():
      return self._is_move_with_rainbow_card_possible(card)
    else:
      return self._is_move_with_regular_card_possible(card)

  def _is_move_with_rainbow_card_possible(self, card : Card):
    return card.offset > 0 or self._can_move_any_turtle_backward()

  def _can_move_any_turtle_backward(self):
    return max([self._find_pos(turtle) for turtle in self.turtles]) > 0
  
  def _is_move_with_regular_card_possible(self, card : Card):
    turtle = Turtle(card.color)
    if turtle not in self.turtles:
      return False
    if card.offset < 0 and self._find_pos(turtle) == 0:
      return False
    return True