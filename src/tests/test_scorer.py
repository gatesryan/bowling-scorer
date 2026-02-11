import pytest
from typing import Literal

from scorer import score_game
from bowling_types import Roll

def test_complete_open_game_all_zeros():
    rolls: list[Roll] = [0, 0] * 10
    assert score_game(rolls) == [0] * 10


def test_complete_open_game_all_nines_and_misses():
    rolls: list[Roll] = [9, 0] * 10
    assert score_game(rolls) == [9] * 10


def test_mixed_complete_game_with_strike_and_spare():
    rolls = [4, 5, "X", 8, "/", 5, 3]
    assert score_game(rolls) == [9, 20, 15, 8]


def test_in_progress_single_roll_open_frame():
    assert score_game([4]) == [None]

def test_perfect_game():
    rolls: list[Roll] = ["X"] * 12
    assert score_game(rolls) == [30] * 10

def test_in_progress_spare_waiting_for_bonus_roll():
    assert score_game([3, "/"]) == [None]

def test_in_progress_strike_waiting_for_two_bonus_rolls():
    assert score_game([4, 5, "X", 8]) == [9, None, None]

def test_invalid_roll_sequence():
    with pytest.raises(ValueError):
        score_game(["X", "/"])

@pytest.mark.parametrize(
    "rolls",
    [
        [11],
        [-1, 5],
        [0, 12, 3],
    ],
)
def test_invalid_roll_values_raise_value_error(rolls):
    with pytest.raises(ValueError):
        score_game(rolls)
