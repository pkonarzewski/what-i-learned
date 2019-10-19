#%%
from enum import Enum
from typing import List, NamedTuple, Callable, Optional
import random
from math import sqrt
# from generic_search import dfs, bfs, node_to_path, Node


class Cell(str, Enum):
    EMPTY = ' '
    BLOCKED = 'X'
    START = 'S'
    GOAL = 'G'
    PATH = '*'


class MazeLocation(NamedTuple):
    row: int
    column: int


class Maze:
    def __init__(self, rows: int = 10, columns: int = 10, sparsness: float = 0.2, start: MazeLocation = MazeLocation(0,0), goal: MazeLocation = MazeLocation(9,9)) -> None:
        self._rows: int = rows
        self._columns = columns
        self.start: MazeLocation = start
        self.goal: MazeLocation = goal

        self._grid: List[List[Cell]] = [[Cell.EMPTY for c in range(columns)] for r in range(rows)]

        self._random_fill(rows, columns, sparsness)
        self._grid[start.row][start.column] = Cell.START
        self._grid[goal.row][goal.column] = Cell.GOAL

    def _random_fill(self, rows: int, columns: int, sparseness:float):
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0, 1.0) < sparseness:
                    self._grid[row][column] = Cell.BLOCKED

    def goal_test(self, ml: MazeLocation) -> bool:
        return ml == self.goal

    def successors(self, ml: MazeLocation) -> List(MazeLocations):
        locations: List[MazeLocation] = []
        if ml.row + 1 < self._rows and self._grid[ml.row + 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row + 1, ml.column))
        if ml.row - 1 < self._rows and self._grid[ml.row - 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row - 1, ml.column))
        if ml.column + 1 < self._rows and self._grid[ml.row][ml.column + 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column + 1))
        if ml.column - 1 < self._rows and self._grid[ml.row][ml.column - 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column - 1))

    def __str__(self) -> str:
        output: str = ''
        for row in self._grid:
            output += ''.join([c.value for c in row]) + '\n'
        return output

maze: Maze = Maze()
print(maze)
#%% DFS


#%%
