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


class SequenceOfBits:

    def __init__(self):
        self.data: int = 1
        self.n: int = -1

    @property
    def bit_length(self):
        return self.data.bit_length() - 1

    @property
    def element_number(self):
        return self.bit_length // 2

    def add(self, value):
        self.data <<= 2
        self.data |= value

    def __iter__(self):
        self.n = -1
        return self

    def __next__(self):
        self.n += 1
        if self.n >= self.element_number:
            raise StopIteration
        return self.__getitem__(self.n)

    def __repr__(self):
        return bin(self.data)

    def __getitem__(self, element_no):
        pos = element_no*2
        if element_no <= self.element_number:
            return self.data >> pos & 0b11
        raise ValueError('Out of index')

# test
sob = SequenceOfBits()
sob.add(0b00)
sob.add(0b01)
sob.add(0b10)
sob.add(0b11)
sob.add(0b00)
sob.add(0b01)
sob.add(0b10)
sob.add(0b11)

print(sob)

for n, s in enumerate(sob):
    assert s == sob[n]

class CompressedGene:

    def __init__(self, gene) -> None:
        self.bit_string: SequenceOfBits = SequenceOfBits()
        self._compress(gene)

    def _compress(self, gene: str) -> None:
        for nucleotide in gene.upper():
            if nucleotide == 'A':
                self.bit_string.add(0b00)
            elif nucleotide == 'C':
                self.bit_string.add(0b01)
            elif nucleotide == 'G':
                self.bit_string.add(0b10)
            elif nucleotide == 'T':
                self.bit_string.add(0b11)
            else:
                raise ValueError(f'Invalid Nucleotide: {nucleotide}')

    def decompress(self) -> str:
        gene: str = ''

        for bits in self.bit_string:
            if bits == 0b00:
                gene += 'A'
            elif bits == 0b01:
                gene += 'C'
            elif bits == 0b10:
                gene += 'G'
            elif bits == 0b11:
                gene += 'T'
            else:
                raise ValueError(f'Invalid bits: {bits}')
        return gene[::-1]

from sys import getsizeof

original: str = "TAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATATAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATA"*100
print('original is {} bytes'.format(getsizeof(original)))
compressed: CompressedGene = CompressedGene(original)
print('compresed is {} bytes'.format(getsizeof(compressed)))
print('are the same: {}'.format(original == compressed.decompress()))
print(original)
print(compressed.decompress())


#%% 3.
"""
Write a solver for The Towers of Hanoi that works for any number of towers.
"""

from typing import TypeVar, Generic, List
T = TypeVar('T')

class Stack(Generic[T]):

    def __init__(self) -> None:
        self._container: List[T] = []

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()

    def __repr__(self) -> str:
        return repr(self._container)

def hanoi(begin, end, temp, n):
    if n == 1:
        end.push(begin.pop())
    else:
        hanoi(begin, temp, end, n-1)
        hanoi(begin, end, temp, 1)
        hanoi(temp, end, begin, n-1)


num_discs: int = 16
num_towers: int = 4

towers = [Stack() for _ in range(num_towers)]
for i in range(1, num_discs + 1):
    towers[0].push(i)

print(towers)
hanoi(towers[0], towers[num_towers-1], towers[num_towers-2], num_discs)
print(towers)


#%% 4.
"""
Use a one-time pad to encrypt and decrypt images.
"""

import os
from secrets import token_bytes

cpath = os.path.dirname(os.path.abspath(__file__))

def random_key(length: int) -> int:
    tb: bytes = token_bytes(length)
    return int.from_bytes(tb, 'big')

def encrypt(original_bytes):
    dummy = random_key(len(original_bytes))
    original_key = int.from_bytes(original_bytes, 'big')
    encrypted = original_key ^ dummy
    return dummy, encrypted

def decrypt(key1, key2):
    decrypted = key1 ^ key2
    temp = decrypted.to_bytes((decrypted.bit_length() +7) // 8, 'big')
    return temp

with open((cpath + '/input_picture.jpg'), 'rb') as image:
    f = image.read()
    f_encrypted = encrypt(f)

with open((cpath + '/input_picture_crypted.jpg'), 'wb') as image:
    image.write(f_encrypted[1].to_bytes((f_encrypted[1].bit_length() +7) // 8, 'big'))

with open(cpath + '/decrypted_picture.jpg', 'wb') as image:
    image.write(decrypt(*f_encrypted))
