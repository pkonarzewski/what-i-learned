import sys
from collections import defaultdict
from pathlib import Path


def load(path: Path) -> tuple[list[tuple[int, int]], list[tuple[int, ...]]]:
    found_separator = False
    page_order = []
    pages = []

    with path.open(mode="r") as f:
        for line in f:
            line = line.strip()
            if line == "":
                found_separator = True
                continue

            if not found_separator:
                page_order.append(tuple(int(x) for x in line.split("|")))
                continue

            if found_separator:
                pages.append(tuple(int(x) for x in line.split(",")))

    return page_order, pages


def is_correct_order(page_order: dict[int, set[int]], pages: tuple[int]) -> bool:
    for i in range(len(pages) - 1):
        node = page_order.get(pages[i], None)

        if node is None:
            return False

        if not set(pages[i + 1 :]).issubset(node):
            return False

    return True


def fix_order_manual(
    page_order: dict[int, set[int]], pages: tuple[int]
) -> tuple[int, ...]:
    reordered = list(pages)

    i = 0
    while i < len(reordered) - 1:
        node = page_order.get(reordered[i], None)

        if node is not None and set(reordered[i + 1 :]).issubset(node):
            i += 1
            continue

        reordered.append(reordered.pop(i))

    return tuple(reordered)


def check_manual_order(page_order, pages_list) -> tuple[int, int]:
    correct_answer = 0
    fixed_answer = 0

    order_graph = defaultdict(set)

    for k, v in page_order:
        order_graph[k].add(v)

    for pages in pages_list:
        if is_correct_order(order_graph, pages):
            correct_answer += pages[len(pages) // 2]
        else:
            fixed_pages = fix_order_manual(order_graph, pages)
            fixed_answer += fixed_pages[len(pages) // 2]

    return correct_answer, fixed_answer


if __name__ == "__main__":
    page_order, pages = load(Path(sys.argv[1]))

    corr_ans, fixed_ans = check_manual_order(page_order, pages)

    print("Answer 1:", corr_ans)
    print("Answer 2:", fixed_ans)
