import re
from pathlib import Path

mul_pattern = re.compile(r"mul\((\d+),(\d+)\)")

enabler = True


def parse_mul(input: str, pos: int) -> tuple[int, int]:
    if match := mul_pattern.match(input[pos:]):
        res = int(match.group(1)) * int(match.group(2))
        return len(match.group(0)), res

    return 1, 0


def run(input: str, use_enabler: bool = False) -> int:
    res = 0
    i = 0
    global enabler

    while i < len(input):
        if input[i : i + 4] == "do()":
            enabler = True
            i += 3
            continue

        if input[i : i + 7] == "don't()":
            enabler = False
            i += 6
            continue

        if input[i : i + 3] == "mul" and (use_enabler is False or enabler):
            offset, mult = parse_mul(input, i)
            i += offset
            res += mult
            continue

        i += 1

    return res


if __name__ == "__main__":
    res = 0
    with (Path.cwd() / "input" / "day03-full").open(mode="r") as f:
        for line in f:
            res += run(line, use_enabler=True)

    print(res)
