import pytest
from src.roulette import (
    Outcome,
    Bin,
    Wheel,
    BinBuilder,
    Bet,
    InvalidBet,
    Table,
    Passenger57,
    Game,
)


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


def test_wheel():
    o1 = Outcome("Red", 1)
    o2 = Outcome("Black", 2)

    wheel = Wheel()
    wheel.add_outcome(8, o1)
    wheel.add_outcome(9, o2)

    assert o1 in wheel.get(8)
    wheel.rng.seed(1)
    assert o1 in wheel.choose()

    assert o1 == wheel.get_outcome("Red")
    assert o2 == wheel.get_outcome("Black")


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
    table.minimum = 10
    assert str(table) == "Table(bets amount=210)"
    assert (
        repr(table)
        == "Table(Bet(amount=10, outcome=Outcome(name='Red', odds=1)), Bet(amount=200, outcome=Outcome(name='Red', odds=1)))"
    )

    with pytest.raises(InvalidBet):
        table.bets = []
        table.place_bet(Bet(1000, o1))
        table.is_valid()

    with pytest.raises(InvalidBet):
        table.bets = []
        table.place_bet(Bet(3, o1))
        table.is_valid()

    for b in table:
        assert isinstance(b, Bet)


def test_passanger57():
    table = Table()
    table.limit = 100
    table.minimum = 1
    wheel = Wheel()
    oc1 = Outcome("Black", 1)
    wheel.add_outcome(2, oc1)
    player = Passenger57(table, wheel)

    player.place_bets()
    assert Bet(1, oc1) in table.bets

    player.win(Bet(1, oc1))
    player.lose(Bet(1, oc1))


def test_game():
    table = Table()
    table.limit = 100
    table.minimum = 1
    wheel = Wheel()
    oc1 = Outcome("Black", 1)
    wheel.add_outcome(2, oc1)
    player = Passenger57(wheel=wheel, table=table)
    game = Game(wheel=wheel, table=table)

    game.cycle(player)
    game.cycle(player)
    game.cycle(player)
