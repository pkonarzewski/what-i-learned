"""
Roulette game simulator.
"""
from dataclasses import dataclass
import random
from enum import Enum
from typing import Iterator, List, Sequence


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


class InvalidBet(Exception):
    pass


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
        self.outcomes = {}

    def add_outcome(self, number: int, outcome: Outcome) -> None:
        """Adds the given Outcome object to the Bin instance with the given number."""
        self.bins[number].add(outcome)
        self.outcomes[outcome.name] = outcome

    def choose(self) -> Bin:
        """Generates a random number between 0 and 37, and returns the randomly
        selected Bin instance.
        """
        return self.rng.choice(self.bins)

    def get(self, bin: int) -> Bin:
        """Returns the given Bin instance from the internal collection."""
        return self.bins[bin]

    def get_outcome(self, name: str) -> Outcome:
        return self.outcomes[name]


class BinBuilder:
    """BinBuilder creates the Outcome instances for all of the 38 individual
    Bin on a Roulette wheel."""

    def build_bins(self, wheel: Wheel) -> None:
        self.add_straight_bets(wheel)
        self.add_split_bets(wheel)
        self.add_street_bets(wheel)
        self.add_corner_bets(wheel)
        self.add_line_bets(wheel)
        self.add_dozen_bets(wheel)
        self.add_column_bets(wheel)
        self.add_even_money_bets(wheel)
        self.add_five_bet(wheel)

    def add_straight_bets(self, wheel: Wheel) -> None:
        for i in range(0, 37):
            wheel.add_outcome(i, Outcome(str(i), Odds.STRAIGHT))
        wheel.add_outcome(37, Outcome("00", Odds.STRAIGHT))

    def add_split_bets(self, wheel: Wheel) -> None:
        """Generate split bets"""
        bet_name = "Split {}-{}"

        # Left-Right pairs
        for row in TABLE_LAYOUT:
            for n in row[:2]:
                wheel.add_outcome(n, Outcome(bet_name.format(n, n + 1), Odds.SPLIT))
                wheel.add_outcome(n + 1, Outcome(bet_name.format(n, n + 1), Odds.SPLIT))

        # Up-Down pairs
        for row in TABLE_LAYOUT[:-1]:
            for n in row:
                wheel.add_outcome(n, Outcome(bet_name.format(n, n + 3), Odds.SPLIT))
                wheel.add_outcome(n + 3, Outcome(bet_name.format(n, n + 3), Odds.SPLIT))

    def add_street_bets(self, wheel):
        """Generate street bets."""
        bet_name = "Street {}-{}-{}"

        for row in TABLE_LAYOUT:
            for n in row:
                wheel.add_outcome(n, Outcome(bet_name.format(*row), Odds.STREET))

    def add_corner_bets(self, wheel):
        """Generate corner bets"""
        bet_name = "Corner {}-{}-{}-{}"

        for row in TABLE_LAYOUT[:-1]:
            for n in row[:-1]:
                bname = bet_name.format(n, n + 1, n + 3, n + 4)
                wheel.add_outcome(n, Outcome(bname, Odds.CORNER))
                wheel.add_outcome(n + 1, Outcome(bname, Odds.CORNER))
                wheel.add_outcome(n + 3, Outcome(bname, Odds.CORNER))
                wheel.add_outcome(n + 4, Outcome(bname, Odds.CORNER))

    def add_line_bets(self, wheel):
        """Generate line bets."""
        bet_name = "Line {}-{}-{}-{}-{}-{}"

        for row in TABLE_LAYOUT[:-1]:
            line_no = [x for x in range(row[0], row[0] + 6)]
            bname = bet_name.format(*line_no)
            for n in line_no:
                wheel.add_outcome(n, Outcome(bname, Odds.LINE))

    def add_dozen_bets(self, wheel):
        """Generate dozen bes"""
        bet_name = "Dozen {}-{}"

        for n in range(1, 37):
            if n <= 12:
                bname = bet_name.format(1, 12)
            elif n <= 24:
                bname = bet_name.format(13, 24)
            else:
                bname = bet_name.format(25, 36)
            wheel.add_outcome(n, Outcome(bname, Odds.DOZEN))

    def add_column_bets(self, wheel):
        """Generate column bets"""
        bet_name = "Column {}"

        for row in TABLE_LAYOUT:
            wheel.add_outcome(row[0], Outcome(bet_name.format(1), Odds.COLUMN))
            wheel.add_outcome(row[1], Outcome(bet_name.format(2), Odds.COLUMN))
            wheel.add_outcome(row[2], Outcome(bet_name.format(3), Odds.COLUMN))

    def add_even_money_bets(self, wheel):
        """Generate even-money bets"""

        for n in range(1, 37):
            if n < 19:
                wheel.add_outcome(n, Outcome("Low", Odds.EVEN))
            else:
                wheel.add_outcome(n, Outcome("High", Odds.EVEN))

            if n % 2 == 0:
                wheel.add_outcome(n, Outcome("Even", Odds.EVEN))
            else:
                wheel.add_outcome(n, Outcome("Odd", Odds.EVEN))

            if n in (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 24, 36):
                wheel.add_outcome(n, Outcome("Red", Odds.EVEN))
            else:
                wheel.add_outcome(n, Outcome("Black", Odds.EVEN))

    def add_five_bet(self, wheel):
        """Generate five bet"""
        bet_name = "00-0-1-2-3"

        for n in range(0, 4):
            wheel.add_outcome(n, Outcome(bet_name, Odds.FIVE))

        # 00
        wheel.add_outcome(37, Outcome(bet_name, Odds.FIVE))


@dataclass
class Bet:
    """Bet associates an amount and an Outcome. In a future round of design,
    we can also associate a Bet with a Player."""

    amount: int
    outcome: Outcome

    def win_amount(self) -> int:
        """Uses the Outcome’s winAmount to compute the amount won, given the amount of this bet"""
        return self.amount + self.amount * self.outcome.odds

    def lose_amount(self) -> int:
        return self.amount

    def __str__(self) -> str:
        return f"Bet(amount={self.amount!r}, outcome={self.outcome!s})"


class Table:

    limit: int
    minimum: int

    def __init__(self, *bets: Bet) -> None:
        self.bets: List[Bet] = [*bets] if bets is not None else []

    def place_bet(self, bet: Bet) -> None:
        self.bets.append(bet)

    def is_valid(self):
        if (
            sum([b.amount for b in self.bets]) > self.limit
            or min([b.amount for b in self.bets]) < self.minimum
        ):
            raise InvalidBet("Invalid Bet")

    def __iter__(self) -> Iterator[Bet]:
        return iter(self.bets)

    def __str__(self) -> str:
        return f"Table(bets amount={sum([b.amount for b in self.bets])!s})"

    def __repr__(self) -> str:
        return f"Table({', '.join([repr(b) for b in self.bets])})"
