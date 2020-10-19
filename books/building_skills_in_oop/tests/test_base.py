import pytest
from fractions import Fraction

from casino.base import Outcome


def test_simple_outcome():
    o1 = Outcome("Red", 1)
    o2 = Outcome("Red", 1)
    o3 = Outcome("Black", 2)
    assert str(o1) == "Red (1:1)"
    assert repr(o2) == "Outcome(name='Red', odds=Fraction(1, 1))"
    assert o1 == o2
    assert o1.odds == Fraction(1, 1)
    assert o1.name == "Red"
    assert o1 != o3
    assert o2 != o3

    assert o1.win_amount(Fraction(5)) == 5
    assert isinstance(o1.win_amount(Fraction(5)), Fraction)
    assert o3.win_amount(Fraction(5)) == 10


def test_fraction_outcome():
    o1 = Outcome("1-2 Split", 17, 3)
    assert str(o1) == "1-2 Split (17:3)"
    assert o1.win_amount(Fraction(17 * 3)) == 289
