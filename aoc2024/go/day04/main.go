package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strings"
)

type Matrix struct {
	Data []string
	X    int
	Y    int
}

func (r Matrix) Get(y int, x int) string {
	return r.Data[r.Y*y+x]
}

func (r Matrix) GetPos(pos int) (y int, x int) {
	return pos / r.Y, pos % r.Y
}

func (r Matrix) FindXmas(pos int) int {
	var foundMatch int
	y, x := r.GetPos(pos)

	if x+4 <= r.X {
		fmt.Println("right")
		foundMatch += r.matchXmas([5]string{r.Data[pos], r.Data[pos+1], r.Data[pos+2], r.Data[pos+3]})
	}

	if x-3 >= 0 {
		fmt.Println("left")
		foundMatch += r.matchXmas([5]string{r.Data[pos], r.Data[pos-1], r.Data[pos-2], r.Data[pos-3]})
	}

	if y+4 <= r.Y {
		fmt.Println("down")
		foundMatch += r.matchXmas([5]string{r.Data[pos], r.Data[pos+1*r.Y], r.Data[pos+2*r.Y], r.Data[pos+3*r.Y]})
	}

	if y-3 >= 0 {
		fmt.Println("up")
		foundMatch += r.matchXmas([5]string{r.Data[pos], r.Data[pos-1*r.Y], r.Data[pos-2*r.Y], r.Data[pos-3*r.Y]})
	}

	if y-3 >= 0 && x+4 <= r.X {
		fmt.Println("up-right")
		foundMatch += r.matchXmas([5]string{r.Data[pos], r.Data[pos+1-1*r.Y], r.Data[pos+2-2*r.Y], r.Data[pos+3-3*r.Y]})
	}

	if y+4 <= r.Y && x-3 >= 0 {
		fmt.Println("down-left")
		foundMatch += r.matchXmas([5]string{r.Data[pos], r.Data[pos-1+1*r.Y], r.Data[pos-2+2*r.Y], r.Data[pos-3+3*r.Y]})
	}

	if y-3 >= 0 && x-3 >= 0 {
		fmt.Println("up-left")
		foundMatch += r.matchXmas([5]string{r.Data[pos], r.Data[pos-1-1*r.Y], r.Data[pos-2-2*r.Y], r.Data[pos-3-3*r.Y]})
	}

	if y+4 <= r.Y && x+4 <= r.X {
		fmt.Println("down-right")
		foundMatch += r.matchXmas([5]string{r.Data[pos], r.Data[pos+1+1*r.Y], r.Data[pos+2+2*r.Y], r.Data[pos+3+3*r.Y]})
	}

	return foundMatch
}

func (r Matrix) matchXmas(vec [5]string) int {
	if vec == [5]string{"X", "M", "A", "S"} {
		// fmt.Println("MATCH", vec)
		return 1
	}
	return 0
}

func (r Matrix) findXmas2(pos int) int {
	expVal := "AMMSS"

	if pos <= r.Y || pos >= len(r.Data)-r.Y || pos%r.Y == 0 || pos%r.Y == r.Y-1 {
		return 0
	}

	if r.Data[pos-1-1*r.Y] == r.Data[pos+1+1*r.Y] {
		return 0
	}

	fmt.Println(r.GetPos(pos))
	vals := []string{"A", r.Data[pos+1-1*r.Y], r.Data[pos+1+1*r.Y], r.Data[pos-1+1*r.Y], r.Data[pos-1-1*r.Y]}
	sort.Strings(vals)
	abc := strings.Join(vals, "")
	fmt.Println(abc)
	if abc == expVal {
		return 1
	}

	return 0
}

func main() {

	matrix, err := input_to_matrix(os.Args[1])

	if err != nil {
		fmt.Println(err)
		return
	}

	var found_xmas1 int
	for i, val := range matrix.Data {
		if val != "X" {
			continue
		}
		found := matrix.FindXmas(i)
		found_xmas1 += found

	}

	fmt.Println("Found XMAS (part 1):", found_xmas1)

	var found_xmas2 int
	for i, val := range matrix.Data {
		if val != "A" {
			continue
		}
		found_xmas2 += matrix.findXmas2(i)

	}

	fmt.Println("Found XMAS (part 2):", found_xmas2)
}

func input_to_matrix(inputName string) (Matrix, error) {
	var matrix []string
	y := 0
	x := 0

	readFile, err := os.Open("input/" + inputName)
	defer readFile.Close()

	if err != nil {
		return Matrix{}, err
	}

	fileScanner := bufio.NewScanner(readFile)
	fileScanner.Split(bufio.ScanLines)

	for fileScanner.Scan() {
		row := fileScanner.Text()

		for _, char := range row {
			matrix = append(matrix, string(char))
		}

		y++
		if x == 0 {
			x = len(row)
		}
	}
	return Matrix{Data: matrix, X: x, Y: y}, nil
}
