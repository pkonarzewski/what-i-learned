from pathlib import Path

vector = ("X", "M", "A", "S")

# Matrix = list[list[int]]
Position = tuple[int, int]


class Matrix:
    def __init__(self, data: list[list[int]]) -> None:
        self._data = data

    @property
    def shape(self) -> tuple[int, int]:
        return len(self._data[0]), len(self._data[1])

    def get(self, y: int, x: int) -> int:
        return self._data[y][x]

    def get_vector(self, y: int, x: int, direction: int):
        m = self._data
        if direction == 0:  # u
            return (
                m[y][x],
                m[y - 1][x],
                m[y - 2][x],
                m[y - 3][x],
            )
        elif direction == 1:  # ur
            return (
                m[y][x],
                m[y - 1][x + 1],
                m[y - 2][x + 2],
                m[y - 3][x + 3],
            )
        elif direction == 2:  # r
            return (
                m[y][x],
                m[y][x + 1],
                m[y][x + 2],
                m[y][x + 3],
            )
        elif direction == 3:  # dr
            return (
                m[y][x],
                m[y + 1][x + 1],
                m[y + 2][x + 2],
                m[y + 3][x + 3],
            )
        elif direction == 4:  # d
            return (
                m[y][x],
                m[y + 1][x],
                m[y + 2][x],
                m[y + 3][x],
            )
        elif direction == 5:  # dl
            return (
                m[y][x],
                m[y + 1][x - 1],
                m[y + 2][x - 2],
                m[y + 3][x - 3],
            )
        elif direction == 6:  # l
            return (
                m[y][x],
                m[y][x - 1],
                m[y][x - 2],
                m[y][x - 3],
            )
        elif direction == 7:  # ul
            return (
                m[y][x],
                m[y - 1][x - 1],
                m[y - 2][x - 2],
                m[y - 3][x - 3],
            )


# direction (8) from 0-7: 0 up, 1 up right


def load(fname: str) -> Matrix:
    res: list[list[int]] = []
    with (Path.cwd() / "input" / fname).open(mode="r") as f:
        for line in f:
            res.append(list(line.strip()))

    return Matrix(res)


def get_vector(matrix: Matrix, pos: Position, direction: int):
    if pos[0] >= 3:
        print(pos)


def run(matrix: Matrix) -> int:
    shape_y, shape_x = matrix.shape

    searched_vectors = []

    for y in range(shape_y):
        for x in range(shape_x):
            if matrix.get(y, x) == "X":
                if y >= 3:
                    searched_vectors.append(matrix.get_vector(y, x, 0))

                if y >= 3 and x + 3 < shape_x:
                    searched_vectors.append(matrix.get_vector(y, x, 1))

                if x + 3 < shape_x:
                    searched_vectors.append(matrix.get_vector(y, x, 2))

                if x + 3 < shape_x and y + 3 < shape_y:
                    searched_vectors.append(matrix.get_vector(y, x, 3))

                if y + 3 < shape_y:
                    searched_vectors.append(matrix.get_vector(y, x, 4))

                if y + 3 < shape_y and x >= 3:
                    searched_vectors.append(matrix.get_vector(y, x, 5))

                if x >= 3:
                    searched_vectors.append(matrix.get_vector(y, x, 6))

                if y >= 3 and x >= 3:
                    searched_vectors.append(matrix.get_vector(y, x, 7))

    return len([x for x in searched_vectors if x == vector])


if __name__ == "__main__":
    res = 0

    matrix = load("day04-test")
    res = run(matrix)
    print(res)
