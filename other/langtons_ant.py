"""
https://en.wikipedia.org/wiki/Langton%27s_ant

Langton's Ant

Rules:
 -At a white square, turn 90° clockwise, flip the color of the square, move forward one unit
- At a black square, turn 90° counter-clockwise, flip the color of the square, move forward one unit
"""
#%%
from typing import List
from dataclasses import dataclass
from enum import Enum

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Direction(tuple, Enum):
    UP = (0, 1)
    RIGHT = (1, 0)
    DOWN = (0, -1)
    LEFT = (-1, 0)


class Ant:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction: Direction = None
        self.state = None

    def move(self, state):
        self.state.move(self)


@dataclass
class Cell:
    color: str


class Board:

    def __init__(self, size_x: int, size_y: int, seed: int=1234, fill_pct: float = 0.3):
        self.size_x = size_x
        self.size_y = size_y
        self.seed = seed
        self.fill_pct = fill_pct
        self.board: np.zeros((size_x, size_y), dtype=int)


#
board = Board(1000, 1000)

m = np.zeros((100, 100))

# dpi = 80.0
figsize = size[1]/float(dpi), size[0]/float(dpi)
fig = plt.figure(figsize=figsize, dpi=dpi)
fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False)
im = plt.imshow(m, interpolation='nearest', cmap=plt.gr, vmin=0, vmax=1)
plt.xticks([]), plt.yticks([])

animation = FuncAnimation(fig, update, interval=10, frames=2000)
plt.show()
# %%
def update(*args):
    pass

m = np.zeros((100, 100))

fig = plt.figure(figsize=(100, 100))
fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False)

animation = FuncAnimation(fig, update, interval=10, frames=2000)
plt.show()


# %%
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def update(*args):
    global Z, M

    N = (Z[0:-2, 0:-2] + Z[0:-2, 1:-1] + Z[0:-2, 2:] +
         Z[1:-1, 0:-2]                 + Z[1:-1, 2:] +
         Z[2:  , 0:-2] + Z[2:  , 1:-1] + Z[2:  , 2:])
    birth = (N == 3) & (Z[1:-1, 1:-1] == 0)
    survive = ((N == 2) | (N == 3)) & (Z[1:-1, 1:-1] == 1)
    Z[...] = 0
    Z[1:-1, 1:-1][birth | survive] = 1

    # Show past activities
    M[M>0.25] = 0.25
    M *= 0.995
    M[Z==1] = 1
    # Direct activity
    # M[...] = Z
    im.set_data(M)


Z = np.random.randint(0, 2, (300, 600))
M = np.zeros(Z.shape)

size = np.array(Z.shape)
dpi = 80.0
figsize = size[1]/float(dpi), size[0]/float(dpi)
fig = plt.figure(figsize=figsize, dpi=dpi)
fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False)
im = plt.imshow(M, interpolation='nearest', cmap=plt.cm.gray_r, vmin=0, vmax=1)
plt.xticks([]), plt.yticks([])

animation = FuncAnimation(fig, update, interval=10, frames=2000)
# animation.save('game-of-life.mp4', fps=40, dpi=80, bitrate=-1, codec="libx264",
#                extra_args=['-pix_fmt', 'yuv420p'],
#                metadata={'artist':'Nicolas P. Rougier'})
plt.show()

# %%
