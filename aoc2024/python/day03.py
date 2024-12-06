import re
from pathlib import Path

mul_pattern = re.compile(r"mul\((\d+),(\d+)\)")


def parse_mul(input: str, pos: int) -> tuple[int, int]:
    if match := mul_pattern.match(input[pos:]):
        res = int(match.group(1)) * int(match.group(2))
        return len(match.group(0)), res

    return 1, 0


def run(input: str) -> int:
    res = 0
    i = 0
    while i < len(input) - 3:
        scan = input[i : i + 3]
        if scan == "mul":
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
            res += run(line)

    print(res)
