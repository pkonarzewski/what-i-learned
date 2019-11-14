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
        """Returns the amount bet as the amount lost. This is the cost of placing the bet."""
        return self.amount

    def __str__(self) -> str:
        return f"Bet(amount={self.amount!r}, outcome={self.outcome!s})"


class Table:
    """Table contains all the Bet instances created by a Player object.
    A table also has a betting limit, and the sum of all of a player’s bets
    must be less than or equal to this limit. We assume a single Player object
    in the simulation.
    """

    limit: int
    minimum: int

    def __init__(self, *bets: Bet) -> None:
        self.bets: List[Bet] = [*bets] if bets is not None else []

    def place_bet(self, bet: Bet) -> None:
        """Adds this bet to the list of working bets."""
        self.bets.append(bet)
        self.is_valid()

    def is_valid(self):
        """If there’s a problem an InvalidBet exception is raised."""
        if (
            sum([b.amount for b in self.bets]) > self.limit
            or min([b.amount for b in self.bets]) < self.minimum
        ):
            raise InvalidBet("Invalid Bet")

    def __iter__(self) -> Iterator[Bet]:
        """Returns an iterator over the available list of Bet instances.
        This simply returns the iterator over the list of Bet objects."""
        return iter(self.bets)

    def __str__(self) -> str:
        return f"Table(bets amount={sum([b.amount for b in self.bets])!s})"

    def __repr__(self) -> str:
        return f"Table({', '.join([repr(b) for b in self.bets])})"


class Player:
    """Player places bets in Roulette. This an abstract class, with no actual
    body for the Player.placeBets() method. However, this class does implement
    the basic Player.win() method used by all subclasses.
    """

    def __init__(self, table: Table, wheel: Wheel) -> None:
        self.table: Table = table
        self.stake: int = -1
        self.rounds_to_go: int = -1

    def playing(self) -> bool:
        raise NotImplementedError()

    def place_bets(self) -> None:
        """Updates the Table object with the various bets.
        This version creates a Bet instance from the “Black” Outcome instance.
        """
        raise NotImplementedError()

    def win(self, bet: Bet) -> None:
        """Notification from the Game object that the Bet instance was a winner."""
        pass

    def lose(self, bet: Bet) -> None:
        """Notification from the Game object that the Bet instance was a loser."""
        pass


class Passenger57(Player):
    """Passenger57 constructs a Bet instance based on the Outcome object named
    "Black". This is a very persistent player."""

    def __init__(self, table: Table, wheel: Wheel) -> None:
        self.table = table
        self.black = wheel.get_outcome("Black")

    def playing(self) -> bool:
        return True

    def place_bets(self) -> None:
        self.table.place_bet(Bet(1, self.black))


class Martingale(Player):
    """Martingale is a Player who places bets in Roulette. This player doubles
    their bet on every loss and resets their bet to a base amount on each win.
    """

    def __init__(self, table: Table, wheel: Wheel):
        self.table = table
        self.loss_count = 0
        self.black = wheel.get_outcome("Black")

    @property
    def bet_multiple(self):
        return 2 ** self.loss_count

    def playing(self) -> bool:
        if self.bet_multiple <= self.table.limit and self.stake >= self.bet_multiple:
            return True
        else:
            return False

    def place_bets(self) -> None:
        self.table.place_bet(Bet(self.bet_multiple, self.black))
        self.stake -= self.bet_multiple

    def win(self, bet: Bet) -> None:
        self.stake += bet.amount + bet.win_amount()
        self.loss_count = 0

    def lose(self, bet: Bet) -> None:
        self.loss_count += 1


@dataclass
class Game:
    """Game manages the sequence of actions that defines the game of Roulette.
    This includes notifying the Player object to place bets, spinning the Wheel
    object and resolving the Bet instances actually present on the Table object.
    """

    wheel: Wheel
    table: Table

    def cycle(self, player: Player) -> None:
        """This will execute a single cycle of play with a given Player."""
        if player.playing():
            player.place_bets()
            winning_bin = self.wheel.choose()
            for bet in self.table:
                if bet.outcome in winning_bin:
                    player.win(bet)
                else:
                    player.lose(bet)
            self.table.bets = []
