"""Common clases for casino project."""
from dataclasses import dataclass
from fractions import Fraction


class InvalidBet(Exception):
    pass


@dataclass(frozen=True)
class Outcome:
    """Outcome contains a single outcome on which a bet can be placed.

    Parameters:
    name – The name of this outcome
    numerator – The payout odds numerator
    denominator - The payout odds denominator
    """

    name: str
    numerator: int
    denominator: int = 1

    def __post_init__(self) -> None:
        object.__setattr__(self, "odds", Fraction(self.numerator, self.denominator))

    def win_amount(self, amount: Fraction) -> Fraction:
        """
        Multiply this Outcome’s odds by the given amount. The product is returned.
        """
        return self.odds * amount

    def __str__(self) -> str:
        return f"{self.name} ({self.odds.numerator}:{self.odds.denominator})"

    def __repr__(self) -> str:
        return f"Outcome(name={self.name!r}, odds={self.odds!r})"
