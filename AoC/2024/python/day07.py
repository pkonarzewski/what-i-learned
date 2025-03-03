import sys
from itertools import product
from pathlib import Path


def parse_line(input: str) -> tuple[int, tuple[int, ...]]:
    res, els = input.split(":")
    els = tuple(map(int, els.strip().split(" ")))

    return int(res), els


def has_result(exp_result: int, elems: tuple[int, ...], possible_ops: list[str]) -> int:
    all_combs = tuple(product(possible_ops, repeat=len(elems) - 1))

    for com in all_combs:
        res = elems[0]
        for i in range(1, len(elems)):
            if com[i - 1] == "+":
                res = res + elems[i]
            elif com[i - 1] == "|":
                res = int(str(res) + str(elems[i]))
            else:
                res = res * elems[i]

        if res == exp_result:
            return res

    return 0


if __name__ == "__main__":
    input_file = Path(".") / sys.argv[1]

    found_res = 0
    found_res_2 = 0

    with input_file.open(mode="r") as f:
        for line in f:
            res, elements = parse_line(line)
            # print(line, res, ops)
            found_res += has_result(res, elements, ["+", "*"])
            found_res_2 += has_result(res, elements, ["+", "*", "|"])

    print("Found correct results:", found_res)
    print("Found correct results 2:", found_res_2)
