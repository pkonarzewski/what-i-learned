from pathlib import Path

exp = set(("M", "S"))


class Matrix:
    def __init__(self, data: list[list[int]]) -> None:
        self._data = data

    @property
    def shape(self) -> tuple[int, int]:
        return len(self._data[0]), len(self._data[1])

    def get(self, y: int, x: int) -> int:
        return self._data[y][x]


# direction (8) from 0-7: 0 up, 1 up right


def load(fname: str) -> Matrix:
    res: list[list[int]] = []
    with (Path.cwd() / "input" / fname).open(mode="r") as f:
        for line in f:
            res.append(list(map(int, line.strip())))

    return Matrix(res)


def run(matrix: Matrix) -> int:
    shape_y, shape_x = matrix.shape

    found_mas = 0

    for y in range(1, shape_y - 1):
        for x in range(1, shape_x - 1):
            if (
                matrix.get(y, x) == "A"
                and set((matrix.get(y - 1, x + 1), matrix.get(y + 1, x - 1))) == exp
                and set((matrix.get(y - 1, x - 1), matrix.get(y + 1, x + 1))) == exp
            ):
                found_mas += 1

    return found_mas


def part2(puzzle_input):
    rows = puzzle_input
    m = len(rows)
    n = len(rows[0])

    def check(r, c):
        if rows[r][c] != "A":
            return False
        ul = rows[r - 1][c - 1]
        ur = rows[r - 1][c + 1]
        dl = rows[r + 1][c - 1]
        dr = rows[r + 1][c + 1]
        return sorted([ul, ur, dl, dr]) == ["M", "M", "S", "S"] and ul != dr

    return sum(check(r, c) for r in range(1, m - 1) for c in range(1, n - 1))


if __name__ == "__main__":
    res = 0

    matrix = load("day04-full")
    res = run(matrix)
    print(res)
