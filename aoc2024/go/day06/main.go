package main

import (
	"bufio"
	"fmt"
	"os"
	"slices"
)

const Floor = false
const Obst = true

var Directions = [4][2]int{{-1, 0}, {0, 1}, {1, 0}, {0, -1}}

func load(inputName string) ([]bool, int, int, error) {
	var input []bool
	var row_len int
	var start_pos int

	readFile, err := os.Open("input/" + inputName)
	defer readFile.Close()

	if err != nil {
		return nil, -1, -1, err
	}

	fileScanner := bufio.NewScanner(readFile)
	fileScanner.Split(bufio.ScanLines)

	i := -1
	for fileScanner.Scan() {
		row := fileScanner.Text()
		row_len = len(row)

		for _, char_rune := range row {
			i++
			char := string(char_rune)
			if char == "." {
				input = append(input, Floor)
			} else if char == "#" {
				input = append(input, Obst)
			} else if char == "^" {
				input = append(input, Floor)
				start_pos = i
			} else {
				return nil, -1, -1, fmt.Errorf("Unknown character %w %w", char, char_rune)
			}
		}

	}
	return input, row_len, start_pos, nil
}

func WalkMyGuard(lab []bool, lab_width int, start_pos int) map[int]bool {
	var visited = map[int]bool{start_pos: true}
	direction := 0

	var pos = start_pos
	for true {
		delta := Directions[direction]
		next_pos := pos + delta[0]*lab_width + delta[1]
		// fmt.Println(pos/lab_width, pos%lab_width, "|", pos, next_pos)

		if next_pos > len(lab) || next_pos < 0 || (delta[0] == 0 && pos/lab_width != next_pos/lab_width) {
			return visited
		}

		if lab[next_pos] == true {
			direction = (direction + 1) % 4
		} else {
			visited[next_pos] = true
			pos = next_pos
		}

	}

	return visited
}

func WalkMyGuardForever(lab []bool, lab_width int, start_pos int, obs_pos int) int {
	direction := 0
	var obs [][2]int

	var pos = start_pos
	for true {
		delta := Directions[direction]
		next_pos := pos + delta[0]*lab_width + delta[1]
		// fmt.Println(pos/lab_width, pos%lab_width, "|", pos, next_pos)

		if next_pos > len(lab) || next_pos < 0 || (delta[0] == 0 && pos/lab_width != next_pos/lab_width) {
			return 0
		}

		if lab[next_pos] == true || next_pos == obs_pos {
			obsWatch := [2]int{pos, next_pos}
			if slices.Contains(obs, obsWatch) {
				return 1
			}
			obs = append(obs, obsWatch)
			direction = (direction + 1) % 4
		} else {
			pos = next_pos
		}

	}
	return 0
}
func main() {
	lab, lab_width, start_pos, err := load(os.Args[1])

	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	// fmt.Println(lab, lab_width, start_pos)
	visited := WalkMyGuard(lab, lab_width, start_pos)
	fmt.Println("Visited tiles:", len(visited))

	noOfCycles := 0
	for pos, _ := range visited {
		if pos != start_pos {
			noOfCycles += WalkMyGuardForever(lab, lab_width, start_pos, pos)
		}
	}
	fmt.Println("Cycles detected:", noOfCycles)

}
