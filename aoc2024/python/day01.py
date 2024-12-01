from collections import Counter
from pathlib import Path


def calculate_distance():
    note_1, note_2 = [], []

    with (Path.cwd() / "input" / "day01").open(mode="r") as f:
        for line in f:
            val1, val2 = map(int, line.split())
            note_1.append(val1)
            note_2.append(val2)

    note_1.sort()
    note_2.sort()

    note_2_cnt = Counter(note_2)
    sim_score = 0

    diff = 0
    for i in range(len(note_1)):
        diff += abs(note_1[i] - note_2[i])

        sim_score += note_1[i] * note_2_cnt.get(note_1[i], 0)

    print(diff)
    print(sim_score)


if __name__ == "__main__":
    calculate_distance()
