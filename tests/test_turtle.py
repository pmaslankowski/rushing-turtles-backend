import pytest

from rushing_turtles.model.turtle import Turtle


def test_should_raise_error_when_turtle_has_invalid_color():
    with pytest.raises(ValueError):
        Turtle('invalid color')
