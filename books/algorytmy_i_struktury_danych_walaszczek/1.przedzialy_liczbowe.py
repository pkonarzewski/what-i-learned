#%%
from math import ceil


#%% liczby parzyste
def find_brute_force(a,b):
    """
    Wyszukanie liczb parzystych w przedziale domkniety <a, b>, metoda bruteforce
    """
    result = []
    for n in range(a,b+1):
        if n % 2 == 0:
            result.append(n)
    return result

def find_by_sequenc(a,b):
    """
    Wyszukiwanie liczb parzystych w przedzial domkniety <a, b>, metoda gdy znamy
    sekwencje jaka da nam kolejne liczby
    """
    result = []
    if a % 2 != 0:
        a += 1

    while a <= b:
        result.append(a)
        a += 2

    return result


print(find_brute_force(1, 10))
print(find_by_sequenc(1, 10))


# %% podzielnosc przez zadane czynniki
def find_div1(a, b, p):
    """
    Wszystkie liczby podzielne w przedziale <a,b> przez jedna z liczby z
    podzbioru p
    """
    result = []

    for i in range(a,b+1):
        for j in p:
            if i % j == 0:
                result.append(i)
                break
    return result

def find_div2(a, b, P):
    """Liczby te będą wielokrotnościami swoich podzielników."""

    P = set([abs(x) for x in P])
    min_p = []
    result = []

    for p in P:
        min_p = ceil(a / p) * p

        for n in range(min_p, b+1, p):
            result.append(n)

    return sorted(list(set(result)))


assert(find_div2(4, 15, [2, 3]) == [4, 6, 8, 9, 10, 12, 14, 15])
assert(find_div2(-4, 13, [3, 4]) == [-4, -3, 0, 3, 4, 6, 8, 9, 12])
assert(find_div2(0, 5, [2, 3]) == [0, 2, 3, 4])


# %% podzielny przez kazdy z czynnikow
def find_div_by_all_1(a, b, P):
    """W przedziale <a,b> liczb całkowitych wyszukać wszystkie liczby podzielne
    przez każdą z liczb z zadanego zbioru P liczb względnie pierwszych."""

    P = set([abs(x) for x in P])
    min_p = []
    result = []
    pprod = 1

    for p in P:
        pprod *= p


    min_p = ceil(a / pprod) * pprod

    for n in range(min_p, b+1, pprod):
        result.append(n)

    return result


assert(find_div_by_all_1(-4, 8, [3]) == [-3, 0, 3, 6])
assert(find_div_by_all_1(0, 22, [3, 7]) == [0, 21])


# %%
def find_not_div(a, b, P):
    """W przedziale <a,b> liczb całkowitych wyszukać wszystkie liczby niepodzielne
    przez żadną z liczb z zadanego zbioru P."""

    P = set([abs(x) for x in P])
    result = []

    for i in range(a, b+1):
        divisible = False
        for p in P:
            if i % p == 0:
                divisible = True
                break

        if not divisible:
            result.append(i)

    return result

assert find_not_div(2, 5, [2, 3, 5]) == []
assert find_not_div(2, 10, [2, 3, 5]) == [7]


# %%
def arithmetic_progression1(a, n, d):
    """Algorytm wyznaczania n kolejnych wyrazów ciągu arytmetycznego."""

    result = []
    for i in range(a, n+1):
        result.append(a+(i-1)*d)
    return result


print(arithmetic_progression1(3, 10, 3))


# %%
