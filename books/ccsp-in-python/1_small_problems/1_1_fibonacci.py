# 1.1

#%%
def fib1(n: int) -> int:
    return fib1(n - 1) + fib1(n - 2)


print(fib1(5))

#%%
def fib2(n: int) -> int:
    if n < 2:  # base case
        return n
    return fib2(n - 2) + fib2(n - 1)


print(fib2(2))
print(fib2(40))


#%%
from typing import Dict

memo: Dict[int, int] = {0: 0, 1: 1}


def fib3(n: int) -> int:
    if n not in memo:
        memo[n] = fib3(n - 1) + fib3(n - 2)
    return memo[n]


print(fib3(40))
print(fib3(50))


#%%
from functools import lru_cache


@lru_cache(maxsize=None)
def fib4(n: int) -> int:
    if n < 2:
        return n
    return fib4(n - 2) + fib4(n - 1)


print(fib4(5))
print(fib4(50))


#%%
def fib5(n: int) -> int:
    if n == 0:
        return n
    last: int = 0
    next: int = 1
    for _ in range(1, n):
        last, next = next, last + next
    return next


print(fib5(5))
print(fib5(50))


#%%
from typing import Generator


def fib6(n: int) -> Generator[int, None, None]:
    yield 0
    if n > 0:
        yield 1
    last: int = 0
    next: int = 1
    for _ in range(1, n):
        last, next = next, last + next
        yield next


print(list(fib6(1)))
print(list(fib6(50)))
