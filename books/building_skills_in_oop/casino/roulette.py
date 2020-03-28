"""
Roulette game simulator.
"""
from dataclasses import dataclass
import random
from enum import Enum
from abc import ABC, abstractmethod
from typing import Iterator, List, Type, Set
from math import sqrt


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
    Wheel contains the 38 individual bins on a Roulette wheel, plus a rng.
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

    def __iter__(self):
        return iter(self.bins)


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

    def add_street_bets(self, wheel: Wheel) -> None:
        """Generate street bets."""
        bet_name = "Street {}-{}-{}"

        for row in TABLE_LAYOUT:
            for n in row:
                wheel.add_outcome(n, Outcome(bet_name.format(*row), Odds.STREET))

    def add_corner_bets(self, wheel: Wheel) -> None:
        """Generate corner bets"""
        bet_name = "Corner {}-{}-{}-{}"

        for row in TABLE_LAYOUT[:-1]:
            for n in row[:-1]:
                bname = bet_name.format(n, n + 1, n + 3, n + 4)
                wheel.add_outcome(n, Outcome(bname, Odds.CORNER))
                wheel.add_outcome(n + 1, Outcome(bname, Odds.CORNER))
                wheel.add_outcome(n + 3, Outcome(bname, Odds.CORNER))
                wheel.add_outcome(n + 4, Outcome(bname, Odds.CORNER))

    def add_line_bets(self, wheel: Wheel):
        """Generate line bets."""
        bet_name = "Line {}-{}-{}-{}-{}-{}"

        for row in TABLE_LAYOUT[:-1]:
            line_no = [x for x in range(row[0], row[0] + 6)]
            bname = bet_name.format(*line_no)
            for n in line_no:
                wheel.add_outcome(n, Outcome(bname, Odds.LINE))

    def add_dozen_bets(self, wheel: Wheel) -> None:
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

    def add_column_bets(self, wheel: Wheel):
        """Generate column bets"""
        bet_name = "Column {}"

        for row in TABLE_LAYOUT:
            wheel.add_outcome(row[0], Outcome(bet_name.format(1), Odds.COLUMN))
            wheel.add_outcome(row[1], Outcome(bet_name.format(2), Odds.COLUMN))
            wheel.add_outcome(row[2], Outcome(bet_name.format(3), Odds.COLUMN))

    def add_even_money_bets(self, wheel: Wheel) -> None:
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

    def add_five_bet(self, wheel: Wheel) -> None:
        """Generate five bet"""
        bet_name = "00-0-1-2-3"

        for n in range(0, 4):
            wheel.add_outcome(n, Outcome(bet_name, Odds.FIVE))

        # 00
        wheel.add_outcome(37, Outcome(bet_name, Odds.FIVE))


@dataclass
class Bet:
    """Bet associates an amount and an Outcome."""

    amount: int
    outcome: Outcome

    def win_amount(self) -> int:
        """Uses the Outcome’s winAmount to compute the amount won"""
        return self.amount + self.amount * self.outcome.odds

    def lose_amount(self) -> int:
        """Returns the amount lost. This is the cost of placing the bet."""
        return self.amount

    def __str__(self) -> str:
        return f"Bet(amount={self.amount!r}, outcome={self.outcome!s})"


class Table:
    """Table contains all the Bet instances created by a Player object.
    A table also has a betting limit, and the sum of all of a player’s bets
    must be less than or equal to this limit. We assume a single Player object
    in the simulation.
    """

    def __init__(self, *bets: Bet) -> None:
        self.bets: List[Bet] = [*bets] if bets is not None else []
        self.limit: int = 0

    def place_bet(self, bet: Bet) -> None:
        """Adds this bet to the list of working bets."""
        self.bets.append(bet)

    def is_valid(self):
        """If there’s a problem an InvalidBet exception is raised."""
        if sum([b.amount for b in self.bets]) > self.limit:
            raise InvalidBet(f"Invalid Bets {self.bets}")

    def __iter__(self) -> Iterator[Bet]:
        """Returns an iterator over the available list of Bet instances.
        This simply returns the iterator over the list of Bet objects."""
        return iter(self.bets)

    def __str__(self) -> str:
        return f"Table(bets amount={sum([b.amount for b in self.bets])!s})"

    def __repr__(self) -> str:
        return f"Table({', '.join([repr(b) for b in self.bets])})"


class Player(ABC):
    """Player places bets in Roulette. This an abstract class, with no actual
    body for the Player.placeBets() method. However, this class does implement
    the basic Player.win() method used by all subclasses.
    """

    def __init__(self, table: Table, wheel: Wheel) -> None:
        self.table: Table = table
        self.stake: int = 0
        self.rounds_to_go: int = 0

    def playing(self) -> bool:
        """Indicate that player is active."""
        if self.stake > 0 and self.rounds_to_go > 0:
            return True
        return False

    @abstractmethod
    def place_bets(self) -> None:
        """Updates the Table object with the various bets.
        This version creates a Bet instance from the “Black” Outcome instance.
        """
        pass

    def win(self, bet: Bet) -> None:
        """Notification from the Game object that the Bet instance was a winner."""
        self.stake += bet.win_amount()

    def lose(self, bet: Bet) -> None:
        """Notification from the Game object that the Bet instance was a loser."""
        pass

    def winners(self, outcomes: Set[Outcome]) -> None:
        """Notife Player about winning outcomes."""
        pass


class Passenger57(Player):
    """Passenger57 constructs a Bet instance based on the Outcome object named
    "Black". This is a very persistent player."""

    def __init__(self, table: Table, wheel: Wheel) -> None:
        self.black = wheel.get_outcome("Black")
        super().__init__(table, wheel)

    def place_bets(self) -> None:
        bet: Bet = min(Bet(10, self.black), self.stake)
        self.table.place_bet(bet)
        self.stake -= bet.lose_amount()


class Martingale(Player):
    """Martingale is a Player who places bets in Roulette. This player doubles
    their bet on every loss and resets their bet to a base amount on each win.
    """

    def __init__(self, table: Table, wheel: Wheel) -> None:
        self.black: Outcome = wheel.get_outcome("Black")
        self.loss_count: int = 0
        super().__init__(table, wheel)

    @property
    def bet_multiple(self) -> int:
        return 2 ** self.loss_count

    def place_bets(self) -> None:
        bet: Bet = Bet(
            min(min(self.bet_multiple, self.table.limit), self.stake), self.black
        )
        self.table.place_bet(bet)
        self.stake -= bet.lose_amount()

    def win(self, bet: Bet) -> None:
        super().win(bet)
        self.loss_count = 0

    def lose(self, bet: Bet) -> None:
        self.loss_count += 1


class SevenReds(Martingale):
    """x."""

    def __init__(self, table: Table, wheel: Wheel) -> None:
        self.table = table
        self.red_count = 7
        self.red_outcome = wheel.get_outcome("Red")
        self.black_outcome = wheel.get_outcome("Black")
        super().__init__(table, wheel)

    def winners(self, outcomes: Set[Outcome]) -> None:
        """x."""
        if self.red_outcome in outcomes:
            self.red_count -= 1
        else:
            self.red_count = 7

    def place_bets(self) -> None:
        if self.red_count <= 0:
            super().place_bets()


class RandomPlayer(Player):
    def __init__(self, table: Table, wheel: Wheel) -> None:
        self.rng = random.Random()
        self.all_oc: List[Outcome] = self.load_outcomes(wheel)
        super().__init__(table, wheel)

    def load_outcomes(self, wheel: Wheel) -> List[Outcome]:
        all_oc: Set[Outcome] = set()
        for bin in wheel:
            all_oc |= bin
        return list(all_oc)

    def place_bets(self) -> None:
        bet: Bet = Bet(10, self.rng.choice(self.all_oc))
        self.table.place_bet(bet)
        self.stake -= bet.lose_amount()


class Player1326State:
    bet_amount: int = 0

    def __init__(self, player: Player) -> None:
        self.player = player

    def current_bet(self) -> Bet:
        return Bet(self.bet_amount, self.player.outcome)

    def next_won(self) -> "Player1326State":
        return NotImplemented

    def next_lost(self) -> "Player1326State":
        return Player1326NoWins(self.player)


class Player1326NoWins(Player1326State):
    def __init__(self, player: Player) -> None:
        self.bet_amount = 1
        super().__init__(player)

    def next_won(self) -> Player1326State:
        return Player1326OneWin(self.player)


class Player1326OneWin(Player1326State):
    def __init__(self, player: Player) -> None:
        self.bet_amount = 3
        super().__init__(player)

    def next_won(self) -> Player1326State:
        return Player1326TwoWins(self.player)


class Player1326TwoWins(Player1326State):
    def __init__(self, player: Player) -> None:
        self.bet_amount = 2
        super().__init__(player)

    def next_won(self) -> Player1326State:
        return Player1326ThreeWins(self.player)


class Player1326ThreeWins(Player1326State):
    def __init__(self, player: Player) -> None:
        self.bet_amount = 6
        super().__init__(player)

    def next_won(self) -> Player1326State:
        return Player1326NoWins(self.player)


class Player1326(Player):
    def __init__(self, table: Table, wheel: Wheel) -> None:
        self.outcome = wheel.get_outcome("Black")
        self.state = Player1326NoWins(self)
        super().__init__(table, wheel)

    def place_bets(self) -> None:
        bet: Bet = self.state.current_bet()
        self.table.place_bet(bet)
        self.stake -= bet.lose_amount()

    def win(self, bet: Bet) -> None:
        super().win(bet)
        self.state = self.state.next_won()

    def lose(self, bet: Bet) -> None:
        self.state = self.state.next_lost()


class CancellationPlayer(Player):
    def __init__(self, table: Table, wheel: Wheel) -> None:
        self.sequence: List[int] = []
        self.reset_sequence()
        self.outcome = wheel.get_outcome("Black")
        super().__init__(table, wheel)

    def reset_sequence(self) -> None:
        self.sequence = [1, 2, 3, 4, 5, 6]

    def place_bets(self) -> None:
        amount = min((self.sequence[0] + self.sequence[-1]), self.stake)
        self.table.place_bet(Bet(amount, self.outcome))
        self.stake -= amount

    def win(self, bet: Bet) -> None:
        super().win(bet)
        self.sequence = self.sequence[1:-1]

    def lose(self, bet: Bet) -> None:
        self.sequence = self.sequence[1:] + [self.sequence[0] + self.sequence[-1]]

    def playing(self) -> bool:
        return super().playing() and len(self.sequence) > 0


class FibonacciPlayer(Player):
    def __init__(self, table: Table, wheel: Wheel) -> None:
        self.recent = 1
        self.previous = 0
        self.outcome = wheel.get_outcome("Black")
        super().__init__(table, wheel)

    def place_bets(self) -> None:
        amount = min(self.recent + self.previous, self.stake)
        self.table.place_bet(Bet(amount, self.outcome))
        self.stake -= amount

    def win(self, bet: Bet) -> None:
        super().win(bet)
        self.recent = 1
        self.previous = 0

    def lose(self, bet: Bet) -> None:
        self.recent, self.previous = self.recent + self.previous, self.recent


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
        player.place_bets()
        self.table.is_valid()
        winning_bin = self.wheel.choose()
        player.winners(winning_bin)
        for bet in self.table:
            if bet.outcome in winning_bin:
                player.win(bet)
            else:
                player.lose(bet)
        self.table.bets = []


class Simulator:
    """Simulator."""

    def __init__(self, game: Game, player: Type[Player]) -> None:
        self.game: Game = game
        self.player: Type[Player] = player
        self.init_duration: int = 250
        self.init_stake: int = 1000
        self.samples: int = 50
        self.durations: IntegerStatistics = IntegerStatistics()
        self.maximas: IntegerStatistics = IntegerStatistics()
        self.last_value: IntegerStatistics = IntegerStatistics()

    def session(self) -> List[int]:
        """x."""
        player = self.player(self.game.table, self.game.wheel)
        player.stake = self.init_stake
        player.rounds_to_go = self.init_duration

        stakes: List[int] = []

        while player.playing():
            self.game.cycle(player)
            stakes.append(player.stake)
            player.rounds_to_go -= 1
        return stakes

    def gather(self) -> None:
        """x."""
        for i in range(self.samples):
            result = self.session()
            self.durations.append(len(result))
            self.maximas.append(max(result))
            self.last_value.append(result[-1])


class IntegerStatistics(list):
    """List that has some descriptive statistics."""

    def mean(self) -> float:
        return sum(self) / len(self)

    def stdev(self) -> float:
        m = self.mean()
        return sqrt(sum((x - m) ** 2 for x in self) / (len(self) - 1))


def main():
    """Execute simulation."""

    wheel = Wheel()
    BinBuilder().build_bins(wheel)
    table = Table()
    table.limit = 1000

    player = SevenReds
    game = Game(wheel, table)

    simulation = Simulator(game, player)
    simulation.init_duration = 2500
    simulation.gather()

    print(
        "Result of simulation:\n"
        f"Strategy: {player.__name__}\n"
        f"Min-Max stake: {min(simulation.maximas)}-{max(simulation.maximas)}\n"
        f"Median stake: {sorted(simulation.maximas)[len(simulation.maximas)//2]}\n"
        f"Stdev: {simulation.maximas.stdev()}\n"
        f"Avg duration: {simulation.durations}\n"
        f"Fin stake: {simulation.last_value}\n"
        f"Max stake: {simulation.maximas}\n"
    )


if __name__ == "__main__":
    main()
