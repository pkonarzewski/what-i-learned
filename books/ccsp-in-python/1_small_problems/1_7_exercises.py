#%% 1.
"""
Write yet another function that solves for element n of the Fibonacci sequence,
using a technique of your own design. Write unit tests that evaluate its correctness
and performance relative to the other versions in this chapter.
"""


def fib(n: int) -> int:
    if n < 2:
        return n
    else:
        return fib(n-2) + fib(n-1)


assert fib(7) == 13
assert fib(10) == 55
assert fib(1) == 1
assert fib(2) == 1
assert fib(3) == 2
print('all good')

#%% 2.
"""
You saw how the simple int type in Python can be used to represent a bit string.
Write an ergonomic wrapper around int that can be used generically as a
sequence of bits (make it iterable and implement __getitem__()). Reimplement
CompressedGene, using the wrapper.
"""


class IntBitter(int):

    def __int__(self):
        pass

    def __iter__(self):
        pass

    def __next__(self):
        pass

    def __getitem__(self):
        pass


#%%
