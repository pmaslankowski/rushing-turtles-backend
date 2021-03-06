import pytest

from rushing_turtles.model.board import Board
from rushing_turtles.model.turtle import Turtle
from rushing_turtles.model.card import Card


def test_move_should_raise_exception_when_turtle_is_not_on_board():
    turtle = Turtle('RED')
    board = Board([])

    with pytest.raises(ValueError):
        board.move(turtle, 1)


def test_turtle_should_be_on_the_first_field_at_init():
    turtle = Turtle('RED')
    board = Board([turtle])

    assert [turtle] in board.start_field


def test_turtle_should_be_on_second_field_when_moved_from_first_to_second():
    turtle = Turtle('RED')
    board = Board([turtle])

    board.move(turtle, 1)
    assert board.further_fields[0] == [turtle]


def test_turtle_shouldnt_be_on_first_when_moved_from_first_to_second():
    turtle = Turtle('RED')
    board = Board([turtle])

    board.move(turtle, 0)

    assert [turtle] not in board.start_field


def test_turtle_stack_should_be_smaller_on_start_when_moved_from_start():
    turtle = Turtle('RED')
    board = Board([turtle])

    board.move(turtle, 0)

    assert len(board.start_field) == 0


def test_turtle_should_move_to_second_field():
    turtle = Turtle('RED')
    board = Board([turtle])

    board.move(turtle, 2)

    assert board.further_fields[1] == [turtle]


def test_turtle_should_move_to_third_field():
    turtle = Turtle('RED')
    board = Board([turtle])

    board.move(turtle, 3)

    assert board.further_fields[2] == [turtle]


def test_turtle_is_in_the_third_field_after_moving_through_the_second():
    turtle = Turtle('RED')
    board = Board([turtle])

    board.move(turtle, 1)
    board.move(turtle, 1)

    assert board.further_fields[1] == [turtle]


def test_turtle_is_not_in_the_second_field_after_moving_through_the_second():
    turtle = Turtle('RED')
    board = Board([turtle])

    board.move(turtle, 1)
    board.move(turtle, 1)

    assert board.further_fields[0] == []


def test_move_moves_to_the_last_field_when_goes_out_of_the_board_from_start():
    turtle = Turtle('RED')
    board = Board([turtle])

    board.move(turtle, 10)

    assert board.further_fields[-1] == [turtle]


def test_move_to_the_last_field_when_goes_out_of_the_board_from_further():
    turtle = Turtle('RED')
    board = Board([turtle])
    board.move(turtle, 1)

    board.move(turtle, 9)

    assert board.further_fields[-1] == [turtle]


def test_move_should_move_turtle_to_finish_from_start():
    turtle = Turtle('RED')
    board = Board([turtle])

    board.move(turtle, 9)

    assert board.further_fields[8] == [turtle]


def test_move_should_move_turtle_to_finish_from_second_field():
    turtle = Turtle('RED')
    board = Board([turtle])

    board.move(turtle, 1)
    board.move(turtle, 8)

    assert board.further_fields[8] == [turtle]


def test_move_raises_exception_when_turtle_tries_to_move_backward_from_start():
    turtle = Turtle('RED')
    board = Board([turtle])

    with pytest.raises(ValueError):
        board.move(turtle, -1)


def test_turtle_should_be_on_start_after_moving_backward_from_second_field():
    turtle = Turtle('RED')
    board = Board([turtle])

    board.move(turtle, 1)
    board.move(turtle, -1)

    assert [turtle] in board.start_field


def test_turtle_shouldnt_be_on_the_same_field_after_moving_backward():
    turtle = Turtle('RED')
    board = Board([turtle])

    board.move(turtle, 1)
    board.move(turtle, -1)

    assert board.further_fields[0] != [turtle]


def test_turtle_should_be_on_second_after_moving_backward_from_third():
    turtle = Turtle('RED')
    board = Board([turtle])

    board.move(turtle, 1)
    board.move(turtle, 1)
    board.move(turtle, -1)

    assert board.further_fields[0] == [turtle]


def test_turtle_shouldnt_be_on_third_after_moving_backward_from_third():
    turtle = Turtle('RED')
    board = Board([turtle])

    board.move(turtle, 1)
    board.move(turtle, 1)
    board.move(turtle, -1)

    assert board.further_fields[1] != [turtle]


def test_two_turtles_should_be_in_separate_stacks_after_init():
    turtle1 = Turtle('RED')
    turtle2 = Turtle('BLUE')
    board = Board([turtle1, turtle2])

    assert [turtle1] in board.start_field
    assert [turtle2] in board.start_field


def test_turtles_should_be_in_the_same_field_in_order_after_move_from_start():
    turtle1 = Turtle('RED')
    turtle2 = Turtle('BLUE')
    board = Board([turtle1, turtle2])

    board.move(turtle1, 1)
    board.move(turtle2, 1)

    assert board.further_fields[0] == [turtle2, turtle1]


def test_turtles_are_in_the_same_field_in_order_after_move_from_further():
    turtle1 = Turtle('RED')
    turtle2 = Turtle('BLUE')
    board = Board([turtle1, turtle2])

    board.move(turtle1, 2)
    board.move(turtle2, 1)
    board.move(turtle2, 1)

    assert board.further_fields[1] == [turtle2, turtle1]


def test_bottom_turtle_should_stay_when_moving_top_turtle_from_further():
    turtle1 = Turtle('RED')
    turtle2 = Turtle('BLUE')
    board = Board([turtle1, turtle2])

    board.move(turtle1, 1)
    board.move(turtle2, 1)
    board.move(turtle2, 1)

    assert board.further_fields[0] == [turtle1]


def test_top_turtle_should_move_when_moving_from_further_fields():
    turtle1 = Turtle('RED')
    turtle2 = Turtle('BLUE')
    board = Board([turtle1, turtle2])

    board.move(turtle1, 1)
    board.move(turtle2, 1)
    board.move(turtle2, 1)

    assert board.further_fields[1] == [turtle2]


def test_two_turtles_should_move_when_moving_bottom_turtle_from_further():
    turtle1 = Turtle('RED')
    turtle2 = Turtle('BLUE')
    board = Board([turtle1, turtle2])

    board.move(turtle1, 1)
    board.move(turtle2, 1)
    board.move(turtle1, 1)

    assert board.further_fields[1] == [turtle2, turtle1]


def test_turtles_should_move_when_moving_bottom_turtle_from_further_to_start():
    turtle1 = Turtle('RED')
    turtle2 = Turtle('BLUE')
    board = Board([turtle1, turtle2])

    board.move(turtle1, 1)
    board.move(turtle2, 1)
    board.move(turtle1, -1)

    assert [turtle2, turtle1] in board.start_field


def test_turtles_should_be_at_second_when_moving_bottom_turtle_from_start():
    turtle1 = Turtle('RED')
    turtle2 = Turtle('BLUE')
    board = Board([turtle1, turtle2])

    board.move(turtle1, 1)
    board.move(turtle2, 1)
    board.move(turtle1, -1)
    board.move(turtle1, 1)

    assert board.further_fields[0] == [turtle2, turtle1]


def test_one_turtle_should_stay_at_start_when_moving_top_turtle_from_start():
    turtle1 = Turtle('RED')
    turtle2 = Turtle('BLUE')
    board = Board([turtle1, turtle2])

    board.move(turtle1, 1)
    board.move(turtle2, 1)
    board.move(turtle1, -1)
    board.move(turtle2, 1)

    assert [turtle1] in board.start_field


def test_three_turtles_two_should_move_to_second_field_when_moving_middle():
    turtle1 = Turtle('RED')
    turtle2 = Turtle('BLUE')
    turtle3 = Turtle('GREEN')
    board = Board([turtle1, turtle2, turtle3])

    board.move(turtle1, 1)
    board.move(turtle2, 1)
    board.move(turtle3, 1)
    board.move(turtle2, 1)

    assert board.further_fields[1] == [turtle3, turtle2]


def test_three_turtles_one_should_stay_in_first_field_when_moving_middle():
    turtle1 = Turtle('RED')
    turtle2 = Turtle('BLUE')
    turtle3 = Turtle('GREEN')
    board = Board([turtle1, turtle2, turtle3])

    board.move(turtle1, 1)
    board.move(turtle2, 1)
    board.move(turtle3, 1)
    board.move(turtle2, 1)

    assert board.further_fields[0] == [turtle1]


def test_is_last_should_return_false_when_board_is_empty():
    turtle = Turtle('RED')
    board = Board([])

    actual = board.is_last(turtle)

    assert not actual


def test_is_last_should_return_true_for_first_turtle():
    turtle = Turtle('RED')
    board = Board([turtle])

    actual = board.is_last(turtle)

    assert actual


def test_is_last_should_return_true_for_turtle_after_move():
    turtle = Turtle('RED')
    board = Board([turtle])

    board.move(turtle, 1)
    actual = board.is_last(turtle)

    assert actual


def test_is_last_should_return_false_when_other_turtle_is_on_start():
    turtle1 = Turtle('RED')
    turtle2 = Turtle('BLUE')
    board = Board([turtle1, turtle2])

    board.move(turtle2, 1)
    actual = board.is_last(turtle2)

    assert not actual


def test_is_last_should_return_true_for_last_turtle():
    turtle1 = Turtle('RED')
    turtle2 = Turtle('BLUE')
    board = Board([turtle1, turtle2])

    board.move(turtle1, 2)
    board.move(turtle2, 1)
    actual = board.is_last(turtle2)

    assert actual


def test_is_last_should_return_false_for_not_last_turtle():
    turtle1 = Turtle('RED')
    turtle2 = Turtle('BLUE')
    board = Board([turtle1, turtle2])

    board.move(turtle1, 2)
    board.move(turtle2, 1)
    actual = board.is_last(turtle1)

    assert not actual


def test_has_anyone_finished_should_return_false_when_all_are_on_start():
    turtle = Turtle('RED')
    board = Board([turtle])

    actual = board.has_anyone_finished()

    assert not actual


def test_has_anyone_finished_returns_false_when_players_are_in_the_middle():
    turtle = Turtle('RED')
    board = Board([turtle])

    board.move(turtle, 5)

    actual = board.has_anyone_finished()

    assert not actual


def test_has_anyone_finished_should_return_true_when_turtle_is_on_finish():
    turtle = Turtle('RED')
    board = Board([turtle])

    board.move(turtle, 9)
    actual = board.has_anyone_finished()

    assert actual


def test_is_move_possible_should_return_false_when_there_are_no_turtles():
    board = Board([])
    card = Card(0, 'RED', 'PLUS')

    actual = board.is_move_with_card_possible(card)

    assert not actual


def test_is_move_possible_returns_false_when_no_turtle_with_given_color():
    board = Board([Turtle('RED')])
    card = Card(0, 'GREEN', 'PLUS')

    actual = board.is_move_with_card_possible(card)

    assert not actual


def test_is_move_possible_should_return_true_when_card_is_forward():
    card = Card(0, 'RED', 'PLUS')
    board = Board([Turtle('RED')])

    actual = board.is_move_with_card_possible(card)

    assert actual


def test_is_move_possible_returns_false_when_backward_card_turtle_on_start():
    card = Card(0, 'RED', 'MINUS')
    board = Board([Turtle('RED')])

    actual = board.is_move_with_card_possible(card)

    assert not actual


def test_is_move_possible_returns_true_when_backward_card_further_turtle():
    card = Card(0, 'RED', 'MINUS')
    turtle = Turtle('RED')
    board = Board([turtle])

    board.move(turtle, 1)
    actual = board.is_move_with_card_possible(card)

    assert actual


def test_is_move_possible_returns_false_when_back_card_turtle_back_on_start():
    card = Card(0, 'RED', 'MINUS')
    turtle1 = Turtle('RED')
    turtle2 = Turtle('BLUE')
    board = Board([turtle1, turtle2])

    board.move(turtle2, 1)
    board.move(turtle1, 1)
    board.move(turtle2, -1)

    actual = board.is_move_with_card_possible(card)

    assert not actual


def test_is_move_possible_returns_false_when_no_turtles_rainbow_card():
    board = Board([])
    card = Card(0, 'RAINBOW', 'PLUS')

    actual = board.is_move_with_card_possible(card)

    assert not actual


def test_is_move_possible_returns_true_when_one_turtle_forward_card():
    board = Board([Turtle('RED')])
    card = Card(0, 'RAINBOW', 'PLUS')

    actual = board.is_move_with_card_possible(card)

    assert actual


def test_is_move_possible_returns_false_when_rainbow_card_turtle_on_start():
    board = Board([Turtle('RED')])
    card = Card(0, 'RAINBOW', 'MINUS')

    actual = board.is_move_with_card_possible(card)

    assert not actual


def test_is_move_possible_returns_true_when_rainbow_card_turtle_on_furter():
    turtle = Turtle('GREEN')
    board = Board([turtle])
    card = Card(0, 'RAINBOW', 'MINUS')

    board.move(turtle, 2)
    actual = board.is_move_with_card_possible(card)

    assert actual


def test_is_move_possible_returns_false_when_rainbow_card_no_turtles():
    board = Board([])
    card = Card(0, 'RAINBOW', 'MINUS')

    actual = board.is_move_with_card_possible(card)

    assert not actual


def test_get_ranking_should_return_turtles_sorted_by_color_when_on_start():
    turtle1 = Turtle('GREEN')
    turtle2 = Turtle('RED')
    board = Board([turtle1, turtle2])

    actual = board.get_ranking()

    assert actual == [turtle2, turtle1]


def test_get_ranking_returns_turtles_sorted_by_position_when_no_stacks():
    turtle1 = Turtle('GREEN')
    turtle2 = Turtle('RED')
    board = Board([turtle1, turtle2])

    board.move(turtle2, 1)
    actual = board.get_ranking()

    assert actual == [turtle2, turtle1]


def test_get_ranking_returns_turtles_sorted_by_pos_when_there_are_stacks():
    turtle1 = Turtle('RED')
    turtle2 = Turtle('GREEN')
    turtle3 = Turtle('YELLOW')
    board = Board([turtle1, turtle2, turtle3])

    board.move(turtle1, 3)
    board.move(turtle2, 2)
    board.move(turtle3, 2)

    actual = board.get_ranking()

    assert actual == [turtle1, turtle3, turtle2]


def test_get_ranking_returns_turtles_sorted_by_position_when_stack_on_start():
    turtles = [Turtle('RED'), Turtle('YELLOW'), Turtle('GREEN'),
               Turtle('PURPLE'), Turtle('BLUE')]

    board = Board(turtles)

    # Turtles 0 and 1 stack on start:
    board.move(turtles[0], 1)
    board.move(turtles[1], 1)
    board.move(turtles[0], -1)

    # Turtles 2 and 3 stack on start:
    board.move(turtles[2], 1)
    board.move(turtles[3], 1)
    board.move(turtles[2], -1)

    board.move(turtles[4], 9)

    actual = board.get_ranking()

    assert actual == [turtles[4], turtles[1], turtles[3], turtles[0],
                      turtles[2]]
