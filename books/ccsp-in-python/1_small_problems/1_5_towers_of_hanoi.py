# 1.5
#%%
from typing import TypeVar, Generic, List
T = TypeVar('T')

#%%
class Stack(Generic[T]):

    def __init__(self) -> None:
        self._container: List[T] = []

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()

    @property
    def empty(self):
        return len(self._container) == 0

    def __repr__(self) -> str:
        return repr(self._container)


def hanoi(begin: Stack[int], end: Stack[int], temp: Stack[int], n: int) -> None:
    if n == 1:
        end.push(begin.pop())
    else:
        hanoi(begin, temp, end, n-1)
        hanoi(begin, end, temp, 1)
        hanoi(temp, end, begin, n-1)


num_discs: int = 4
tower_a: Stack[int] = Stack()
tower_b: Stack[int] = Stack()
tower_c: Stack[int] = Stack()

for i in range(1, num_discs+1):
    tower_a.push(i)

print('start >>', tower_a, tower_b, tower_c)

hanoi(tower_a, tower_c, tower_b, num_discs)

print('end >>', tower_a, tower_b, tower_c)


#%% Hanoi printer

def tower(disk_numbers, source, auxilary, destination):
    if disk_numbers == 1:
        print(f"{source} -> {destination}: {disk_numbers}")
        return
    else:
        tower(disk_numbers - 1, source, destination, auxilary)
        print(f"{source} -> {destination}: {disk_numbers}")
        tower(disk_numbers - 1, auxilary, source, destination)


tower(3, 'source', 'aux', 'dest')
