
#%% PROBLEM 1
"""
PROBLEM 1
If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9.
The sum of these multiples is 23.
Find the sum of all the multiples of 3 or 5 below 1000.
"""

# simple
def problem1_simple(n):
    result = 0

    for i in range(1, n):
        if i % 3 == 0 or i % 5 == 0:
            result += i
    return result

assert problem1_simple(10) == 23
print(problem1_simple(1000))


# functional approach
assert sum([x for x in range(1,10) if x % 3 == 0 or x % 5 == 0]) == 23
print(sum([x for x in range(1,10) if x % 3 == 0 or x % 5 == 0]))


# using geometric/arithmetic aproach
def problem1_alternative(n, p):
    N = (p-1) // n
    return n*(N*(N+1)//2)

assert problem1_alternative(3, 10) + problem1_alternative(5, 10) - problem1_alternative(15, 10) == 23
print(problem1_alternative(3, 1000) + problem1_alternative(5, 1000) - problem1_alternative(15, 1000))


# BENCHMARK
bench_n = 100000
print('simple')
%timeit problem1_simple(bench_n)
print('functional')
%timeit sum([x for x in range(1, bench_n) if x % 3 == 0 or x % 5 == 0])
print('alternative')
%timeit problem1_alternative(3, bench_n) + problem1_alternative(5, bench_n) - problem1_alternative(15, bench_n)


#%% PROBLEM 2
