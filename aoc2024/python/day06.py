import sys
from pathlib import Path

FLOOR = 0
OBST = 1


def load(path: Path) -> tuple[list[int], int, int]:
    lab: list[int] = []
    start_pos: int = -1
    lab_width: int = -1

    with path.open(mode="r") as f:
        for line in f:
            lab_width = len(line.strip())
            for char in line.strip():
                match char:
                    case ".":
                        lab.append(FLOOR)
                    case "#":
                        lab.append(OBST)
                    case "^":
                        lab.append(FLOOR)
                        start_pos = len(lab) - 1
                    case _:
                        raise ValueError(f"Unknown char {char!r}.")

    if start_pos == -1 or lab_width == -1:
        raise ValueError("eeee")

    return lab, lab_width, start_pos


def walk_my_guard(lab: list[int], lab_width: int, start_pos: int) -> int:
    visited: set[int] = {start_pos}
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    cdir = 0

    pos = start_pos

    i = 0
    while True:
        i += 1
        delta = directions[cdir]
        next_pos = pos + delta[0] * lab_width + delta[1]
        print(pos // lab_width, ":", pos % lab_width, "-", pos)

        if (
            next_pos > len(lab)
            or next_pos < 0
            or (delta[0] == 0 and (pos // lab_width != next_pos // lab_width))
        ):
            return len(visited)

        if lab[next_pos] == FLOOR:
            visited.add(next_pos)
        elif lab[next_pos] == OBST:
            cdir = (cdir + 1) % 4
            continue

        pos = next_pos


if __name__ == "__main__":
    lab, lab_width, start_pos = load(Path(sys.argv[1]))
    # print(lab, start_pos)
    visited_tiles = walk_my_guard(lab, lab_width, start_pos)

    print("Visited tiles by guard:", visited_tiles)
