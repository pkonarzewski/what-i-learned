from math import floor,ceil, sqrt, factorial


def is_prime(n):
    if n < 2:
        return False
    else:
        for i in range(2, floor(sqrt(n)+1)):
            if n % i == 0:
                return False
        return True


def factorization(n):
    factors = []

    if n > 100:
        asymptot = ceil(sqrt(n))
    else:
        asymptot = n

    for i in range(2, asymptot + 1):
        if n % i == 0:
            if is_prime(i):
                factors.append(i)

    return factors


def product_of_list(seq):
    prod = 1
    for n in seq:
        prod *= n
    return prod
