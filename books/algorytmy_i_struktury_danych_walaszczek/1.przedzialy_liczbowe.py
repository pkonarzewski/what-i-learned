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
def is_div1(a, b, p):
    """
    Wszystkie liczby w przedziale w przedziale <a,b> przez jedna z liczby z
    podzbioru p
    """
    result = []

    for i in range(a,b+1):
        for j in p:
            if i % j == 0:
                result.append(i)
                break
    return result

def is_div2(a, b, p):
    result = []
    v = []
    p = set([abs(x) for x in p])

    return result


print(is_div1(-100, 100, [5, 12, 17]))
print(is_div2(-100, 100, [5, 12, 17]))

# %%