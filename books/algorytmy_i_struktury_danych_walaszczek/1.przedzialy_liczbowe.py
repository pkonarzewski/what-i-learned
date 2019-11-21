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
