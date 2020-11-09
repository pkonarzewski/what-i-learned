import pytest
from unittest.mock import Mock
from casino.roulette import (
    Bet,
    Bin,
    BinBuilder,
    CancellationPlayer,
    FibonacciPlayer,
    Game,
    IntegerStatistics,
    InvalidBet,
    Martingale,
    Outcome,
    Passenger57,
    Player1326,
    Player1326NoWins,
    Player1326OneWin,
    Player1326ThreeWins,
    Player1326TwoWins,
    RandomPlayer,
    SevenReds,
    Simulator,
    Table,
    Wheel,
)


def test_bin():
    o1 = Outcome("Red", 1)
    o2 = Outcome("Black", 2)

    b1 = Bin([o1, o2])
    b2 = Bin([o1])

    assert len(b1) == 2
    assert len(b2) == 1

    assert o1 in b1
    assert o2 not in b2


def test_wheel():
    mock_rng = Mock(choice=Mock(return_value="bin1"))

    bins = ["bin1", "bin2"]
    wheel = Wheel()
    wheel.bins = bins
    wheel.rng = mock_rng

    value = wheel.choose()
    assert value == "bin1"
    mock_rng.choice.assert_called_with(bins)

    for b in wheel:
        assert isinstance(b, str)


def test_bin_builder_full():
    wheel = Wheel()
    bb = BinBuilder()
    bb.build_bins(wheel)


def test_bin_builder_bets():
    wheel = Wheel()
    bb = BinBuilder()

    # straight bet
    bb.add_straight_bets(wheel)
    assert Outcome("0", 35) in wheel.get(0)
    assert Outcome("00", 35) in wheel.get(37)
    assert Outcome("1", 35) in wheel.get(1)
    assert Outcome("36", 35) in wheel.get(36)

    # split bets
    bb.add_split_bets(wheel)
    assert Outcome("Split 1-2", 17) in wheel.get(1)
    assert Outcome("Split 1-4", 17) in wheel.get(1)

    # street
    bb.add_street_bets(wheel)
    assert Outcome("Street 1-2-3", 11) in wheel.get(1)
    assert Outcome("Street 34-35-36", 11) in wheel.get(36)

    # corner
    bb.add_corner_bets(wheel)
    oc1 = Outcome("Corner 1-2-4-5", 8)
    oc2 = Outcome("Corner 4-5-7-8", 8)
    oc3 = Outcome("Corner 2-3-5-6", 8)
    oc4 = Outcome("Corner 5-6-8-9", 8)
    assert oc1 in wheel.get(1)
    assert oc1 and oc2 in wheel.get(4)

    assert oc1 and oc2 and oc3 and oc4 in wheel.get(5)

    # line
    bb.add_line_bets(wheel)
    oc1 = Outcome("Line 1-2-3-4-5-6", 5)
    oc2 = Outcome("Line 4-5-6-7-8-9", 5)
    assert oc1 in wheel.get(1)
    assert oc1 and oc2 in wheel.get(4)

    # dozen
    bb.add_dozen_bets(wheel)
    assert Outcome("Dozen 1-12", 2) in wheel.get(1)
    assert Outcome("Dozen 13-24", 2) in wheel.get(17)
    assert Outcome("Dozen 25-36", 2) in wheel.get(36)

    # column
    bb.add_column_bets(wheel)
    assert Outcome("Column 1", 2) in wheel.get(1)
    assert Outcome("Column 2", 2) in wheel.get(17)
    assert Outcome("Column 3", 2) in wheel.get(36)

    # even money
    bb.add_even_money_bets(wheel)
    oc_low = Outcome("Low", 1)
    oc_high = Outcome("High", 1)
    oc_red = Outcome("Red", 1)
    oc_black = Outcome("Black", 1)
    oc_even = Outcome("Even", 1)
    oc_odd = Outcome("Odd", 1)
    assert oc_low and oc_red and oc_odd in wheel.get(1)
    assert oc_high and oc_black and oc_odd in wheel.get(17)
    assert oc_high and oc_red and oc_even in wheel.get(36)

    # five
    bb.add_five_bet(wheel)
    oc = Outcome("00-0-1-2-3", 6)
    assert oc in wheel.get(0)
    assert oc in wheel.get(37)


def test_bet():
    b1 = Bet(10, Outcome("Test1", 12))
    assert b1.win_amount() == 130
    assert b1.lose_amount() == 10
    b2 = Bet(5, Outcome("Test2", 1))
    assert b2.win_amount() == 10
    assert b2.lose_amount() == 5
    assert str(b2) == "Bet(amount=5, outcome=Test2 (1:1))"


def test_invalidbet_exception():
    with pytest.raises(InvalidBet):
        raise InvalidBet("TEST")


def test_table():
    o1 = Outcome("Red", 1)

    table = Table(Bet(10, o1), Bet(200, o1))
    table.limit = 300
    assert str(table) == "Table(bets amount=210)"
    assert repr(table) == (
        "Table(Bet(amount=10, outcome=Outcome(name='Red', odds=Fraction(1, 1))), "
        "Bet(amount=200, outcome=Outcome(name='Red', odds=Fraction(1, 1))))"
    )

    with pytest.raises(InvalidBet):
        table.bets = []
        table.bets.append(Bet(1000, o1))
        table.is_valid()

    for b in table:
        assert isinstance(b, Bet)


def test_passanger57():
    table = Table()
    table.limit = 100
    wheel = Wheel()
    oc1 = Outcome("Black", 1)
    wheel.add_outcome(2, oc1)
    player = Passenger57(table, wheel)
    player.stake = 100

    player.place_bets()
    assert Bet(10, oc1) in table.bets

    player.win(Bet(1, oc1))
    player.lose(Bet(1, oc1))


def test_game():
    table = Table()
    table.limit = 100
    wheel = Wheel()
    oc1 = Outcome("Black", 1)
    wheel.add_outcome(2, oc1)
    player = Passenger57(wheel=wheel, table=table)
    game = Game(wheel=wheel, table=table)

    game.cycle(player)
    game.cycle(player)
    game.cycle(player)


def test_martingale():
    table = Table()
    table.limit = 10

    wheel = Wheel()
    ocr = Outcome("Red", 1)
    ocb = Outcome("Black", 1)
    wheel.add_outcome(1, ocr)
    wheel.add_outcome(2, ocb)
    wheel.rng = Mock(choice=Mock(return_value={ocr}))

    player = Martingale(wheel=wheel, table=table)
    player.stake = 100
    assert player.loss_count == 0
    assert player.bet_multiple == 1

    game = Game(wheel=wheel, table=table)

    assert player.stake == 100
    # 1st loose  2^0
    game.cycle(player)
    assert player.stake == 99
    assert player.loss_count == 1
    assert player.bet_multiple == 2
    # 2nd loose 2^1
    game.cycle(player)
    assert player.stake == 97
    assert player.loss_count == 2
    assert player.bet_multiple == 4
    # 3rd loose 2^2
    game.cycle(player)
    assert player.stake == 93
    assert player.loss_count == 3
    assert player.bet_multiple == 8
    # 4th loose - 2^3
    game.cycle(player)
    assert player.stake == 85
    assert player.loss_count == 4
    assert player.bet_multiple == 16
    # 1st win (hit table limit))
    wheel.rng = Mock(choice=Mock(return_value={ocb}))
    game.cycle(player)
    assert player.stake == 95
    assert player.loss_count == 0
    assert player.bet_multiple == 1


def test_seven_reds():

    table = Table()
    table.limit = 100

    wheel = Wheel()
    ocr = Outcome("Red", 1)
    ocb = Outcome("Black", 1)
    wheel.add_outcome(1, ocr)
    wheel.add_outcome(2, ocb)

    game = Game(wheel=wheel, table=table)

    player = SevenReds(wheel=wheel, table=table)
    player.stake = 100

    # check no bets
    wheel.rng = Mock(choice=Mock(return_value={ocb}))
    for _ in range(8):
        game.cycle(player)
        assert player.red_count == 7
        assert player.stake == 100

    wheel.rng = Mock(choice=Mock(return_value={ocr}))
    for i in range(7):
        assert player.red_count == 7 - i
        game.cycle(player)
        assert player.stake == 100

    game.cycle(player)
    assert player.stake == 99
    assert player.loss_count == 1
    assert player.red_count == -1

    game.cycle(player)
    assert player.stake == 97
    assert player.loss_count == 2
    assert player.red_count == -2

    wheel.rng = Mock(choice=Mock(return_value={ocb}))
    game.cycle(player)
    assert player.stake == 101
    assert player.loss_count == 0
    assert player.red_count == 7


def test_player1326():

    wheel = Wheel()
    ocr = Outcome("Red", 1)
    ocb = Outcome("Black", 1)
    wheel.add_outcome(0, ocb)
    wheel.add_outcome(1, ocr)
    table = Table()
    table.limit = 100

    player = Player1326(table, wheel)
    player.stake = 100
    player.rounds_to_go = 100

    nowin = Player1326NoWins(player)
    base_amount = nowin.current_bet().amount

    onewin = Player1326OneWin(player)
    assert onewin.current_bet().amount / base_amount == 3
    twowin = Player1326TwoWins(player)
    assert twowin.current_bet().amount / base_amount == 2
    threewin = Player1326ThreeWins(player)
    assert threewin.current_bet().amount / base_amount == 6

    # simulate game

    game = Game(wheel, table)
    wheel.rng = Mock(choice=Mock(return_value={ocb}))

    assert isinstance(player.state, Player1326NoWins)
    game.cycle(player)
    assert isinstance(player.state, Player1326OneWin)
    game.cycle(player)
    assert isinstance(player.state, Player1326TwoWins)
    game.cycle(player)
    assert isinstance(player.state, Player1326ThreeWins)
    game.cycle(player)
    assert isinstance(player.state, Player1326NoWins)
    game.cycle(player)
    game.cycle(player)
    wheel.rng = Mock(choice=Mock(return_value={ocr}))
    game.cycle(player)
    assert isinstance(player.state, Player1326NoWins)


def test_random_player():

    table = Table()
    table.limit = 100

    wheel = Wheel()
    ocr = Outcome("Red", 1)
    ocb = Outcome("Black", 1)
    wheel.add_outcome(1, ocr)
    wheel.add_outcome(2, ocb)

    game = Game(wheel=wheel, table=table)

    player = RandomPlayer(wheel=wheel, table=table)
    player.stake = 100
    player.rng = Mock(choice=Mock(return_value={ocb}))
    game.cycle(player)


def test_cancellation_player():
    table = Table()
    table.limit = 100

    wheel = Wheel()
    ocr = Outcome("Red", 1)
    ocb = Outcome("Black", 1)
    wheel.add_outcome(1, ocr)
    wheel.add_outcome(2, ocb)

    player = CancellationPlayer(wheel=wheel, table=table)
    player.stake = 100
    player.rounds_to_go = 100

    game = Game(wheel=wheel, table=table)
    wheel.rng = Mock(choice=Mock(return_value={ocb}))

    assert player.playing() is True
    game.cycle(player)
    assert player.stake == 107
    game.cycle(player)
    assert player.stake == 114
    game.cycle(player)
    assert player.stake == 121
    assert player.playing() is False

    player.reset_sequence()
    player.stake = 100
    assert player.playing() is True
    wheel.rng = Mock(choice=Mock(return_value={ocr}))
    game.cycle(player)
    assert player.stake == 93
    game.cycle(player)
    assert player.stake == 84
    game.cycle(player)
    assert player.stake == 72

    wheel.rng = Mock(choice=Mock(return_value={ocb}))
    game.cycle(player)
    assert player.stake == 88


def test_fibonacci_player():
    table = Table()
    table.limit = 100

    wheel = Wheel()
    ocr = Outcome("Red", 1)
    ocb = Outcome("Black", 1)
    wheel.add_outcome(1, ocr)
    wheel.add_outcome(2, ocb)

    player = FibonacciPlayer(wheel=wheel, table=table)
    player.stake = 100
    player.rounds_to_go = 100

    game = Game(wheel=wheel, table=table)
    wheel.rng = Mock(choice=Mock(return_value={ocb}))

    game.cycle(player)
    assert player.stake == 101
    game.cycle(player)
    assert player.stake == 102

    wheel.rng = Mock(choice=Mock(return_value={ocr}))

    game.cycle(player)
    assert player.stake == 101
    game.cycle(player)
    assert player.stake == 99
    game.cycle(player)
    assert player.stake == 96
    game.cycle(player)
    assert player.stake == 91

    wheel.rng = Mock(choice=Mock(return_value={ocb}))
    game.cycle(player)
    assert player.stake == 99
    game.cycle(player)
    assert player.stake == 100


def test_simulator():

    table = Table()
    table.limit = 100

    wheel = Wheel()
    ocr = Outcome("Red", 1)
    ocb = Outcome("Black", 1)
    wheel.add_outcome(1, ocr)
    wheel.add_outcome(2, ocb)

    game = Game(wheel=wheel, table=table)

    player = Passenger57
    player.stake = 100

    sim = Simulator(game, player)

    sim.session()

    sim.gather()


def test_integer_statistics():

    test_data = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]

    istats = IntegerStatistics(test_data)

    assert sum(istats) == 99
    assert len(istats) == 11
    assert istats.mean() == 9.0
    assert round(istats.stdev(), 3) == 3.317
