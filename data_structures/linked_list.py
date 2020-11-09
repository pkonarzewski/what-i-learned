"""
Linked List

access
add
delete
len
reverse
"""
#%%
from typing import Any, Union
from dataclasses import dataclass


@dataclass
class Node:
    value: Any
    next: Union[int, None] = None


@dataclass
class SingleLinkedList:
    head: Union[Node, None] = None

    def add(self, value: Any, position: Union[int, None] = None) -> None:
        """Add element."""
        if self.head is None and position is None:
            self.head = Node(value)
        else:
            position = position - 1 if position is not None else len(self) - 1
            cur = self.get(position)
            node = Node(value)
            node.next = cur.next
            cur.next = node

    def remove(self, position):
        if self.head is None and position is None:
            pass
        else:
            node_to_delete = self.get(position)
            prev_node = self.get(position-1)  # TODO: fix position = 0
            prev_node.next = node_to_delete.next

    def get(self, position):
        for n, cur in enumerate(self):
            if n == position:
                return cur
        raise ValueError(f"Position '{position}' out of range")

    def reverse(self):
        """Reverse list inplace."""
        for cur in self:
            pass

    def __iter__(self) -> Node:
        cur = self.head
        while cur is not None:
            yield cur
            cur = cur.next

    def __len__(self) -> int:
        for n, _ in enumerate(self, 1):
            pass
        return n

    def __str__(self) -> str:
        res = "HEAD -> "
        # return "HEAD -> " + " -> ".join(self) + " -> None"

        for x in ll:
            res += f"{x.value!r} -> "
        res += "None"
        return res


def reversed(linkl):
    """Reverse list."""
    for node in linkl:
        nnn = node.next
        nnn.next = node
        node.next =



# TESTS
ll = SingleLinkedList()

ll.add("Dddd")
ll.add("GrrWrr")

# print(ll)

print(len(ll))

print(ll)

ll.add("Yo", 1)
print(ll)

ll.add("YoZiom", 1)
print(ll)

ll.get(1)

ll.remove(1)
print(ll)


# %%
