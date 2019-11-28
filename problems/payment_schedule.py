#%%
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Schedule:
    id: int
    checked_at: datetime
    installments: list

    def add_payment(self, payment):
        pass


@dataclass
class Installment:
    id: int
    owing_date: datetime
    due_date: datetime
    capital_init: int
    income_init: int
    capital_left: int
    income_left: int
    # penalty_init: int
    # penalty_left: int


@dataclass
class Payment:
    id: int
    created_at: datetime
    amount: int

    def deduct(self, amt):
        self.amount -= amt


s = Schedule(id=1, checked_at=datetime(2019, 9, 2), installments=[Installment(1, datetime(2019, 9, 1), datetime(2019, 10, 1), 100, 20, 100, 20)])
p = Payment(1, datetime(2019, 9, 2), 119)

s.add_payment(p)


#%%









# is_owing
# is_cleared


@dataclass
class Component:
    id: int
    name: str
    amount_init: int
    amount_left: int

# deduct
# write_off
# cancelled


@dataclass
class Event:
    pass


@dataclass
class Payment:
    pass


@dataclass
class PaymentDistriburion:
    pass


#%%
