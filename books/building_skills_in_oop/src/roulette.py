"""
Roulette game simulator.
"""
from dataclasses import dataclass


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
