"""
Roulette game simulator.
"""
from dataclasses import dataclass
import random
from enum import Enum


class Odds(int, Enum):
    STRAIGHT = 35
    SPLIT = 17
    STREET = 11
    CORNER = 8
    FIVE = 6
    LINE = 5
    DOZEN = 2
    COLUMN = 2
    EVEN = 1


TABLE_LAYOUT = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 9),
    (10, 11, 12),
    (13, 14, 15),
    (16, 17, 18),
    (19, 20, 21),
    (22, 23, 24),
    (25, 26, 27),
    (28, 29, 30),
    (31, 32, 33),
    (34, 35, 36),
)


@dataclass(frozen=True)
class Outcome:
    """Outcome contains a single outcome on which a bet can be placed.

    Parameters:
    name (str) – The name of this outcome
    odds (int) – The payout odds of this outcome.
    """

    name: str
    odds: int

    def win_amount(self, amount: float) -> float:
        """
        Multiply this Outcome’s odds by the given amount. The product is returned.
        """
        return self.odds * amount

    def __str__(self):
        return f"{self.name} ({self.odds}:1)"

    def __repr__(self):
        return f"Outcome(name={self.name!r}, odds={self.odds!r})"


class Bin(set):
    """Bin contains a collection of Outcome instances which reflect the winning
    bets that are paid for a particular bin on a Roulette wheel.
    In Roulette, each spin of the wheel has a number of Outcome instances.

    """


class Wheel:
    """
    Wheel contains the 38 individual bins on a Roulette wheel, plus a random number generator.
    It can select a Bin at random, simulating a spin of the Roulette wheel.
    """

    def __init__(self):
        self.bins = list(Bin() for _ in range(38))
        self.rng = random.Random()

    def add_outcome(self, number: int, outcome: Outcome) -> None:
        """Adds the given Outcome object to the Bin instance with the given number."""
        self.bins[number].add(outcome)

    def choose(self) -> Bin:
        """Generates a random number between 0 and 37, and returns the randomly
        selected Bin instance.
        """
        return self.rng.choice(self.bins)

    def get(self, bin: int) -> Bin:
        """Returns the given Bin instance from the internal collection."""
        return self.bins[bin]
