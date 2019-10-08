# %% Type annotations
# from __future__ import annotations
from typing import List


class A(object):
    def __init__() -> None:
        self.elements : List[int] = []

    def add(element: int) -> None:
        self.elements.append(element)


# You can control pylint with comments in code
# pylint: disable=function-redefined
