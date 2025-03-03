from pathlib import Path

# dia  <- vim


def show_rep_pos(report: tuple[int, ...], pos: int):
    res = ""
    for i, v in enumerate(report):
        if i == pos:
            res += f"[{v}] "
            continue
        res += f"{v} "
    print(res)


def validate_report(report: tuple[int, ...], use_dumper: bool = False) -> int:
    for i in range(1, len(report) - 1):
        diffs = (report[i - 1] - report[i], report[i + 1] - report[i])
        show_rep_pos(report, i)

        if (
            tuple(filter(lambda x: abs(x) > 3 or x == 0, diffs))
            or len(tuple(filter(lambda x: x > 0, diffs))) != 1
        ):
            if use_dumper:
                if (
                    validate_report(
                        tuple(report[:i] + report[i + 1 :]), use_dumper=False
                    )
                    is True
                    or validate_report(
                        tuple(report[: i - 1] + report[i:]), use_dumper=False
                    )
                    is True
                    or validate_report(
                        tuple(report[: i + 1] + report[i + 2 :]), use_dumper=False
                    )
                    is True
                ):
                    return True

            return False

    return True


if __name__ == "__main__":
    valid_cnt = 0

    with (Path.cwd() / "input" / "day02").open(mode="r") as f:
        for i, line in enumerate(f, start=1):
            input = tuple(map(int, line.split()))
            print(f"CASE {i}: {input}")
            res = validate_report(input, use_dumper=True)
            print(f"Valid: {int(res)}")
            valid_cnt += res

    print(f"Valid reports: {valid_cnt}")
