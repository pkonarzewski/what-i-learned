import pytest
from src.roulette import Outcome, Bin


def test_outcome():
    o1 = Outcome("Red", 1)
    o2 = Outcome("Red", 1)
    o3 = Outcome("Black", 2)
    assert str(o1) == "Red (1:1)"
    assert repr(o2) == "Outcome(name='Red', odds=1)"
    assert o1 == o2
    assert o1.odds == 1
    assert o1.name == "Red"
    assert o1 != o3
    assert o2 != o3

    assert o1.win_amount(5) == 5
    assert o3.win_amount(5) == 10


def test_bin():
    o1 = Outcome("Red", 1)
    o2 = Outcome("Black", 2)

    b1 = Bin([o1, o2])
    b2 = Bin([o1])

    assert len(b1) == 2
    assert len(b2) == 1

    assert o1 in b1
    assert o2 not in b2
