package main

import (
	"bufio"
	"fmt"
	"os"
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
		fmt.Println("MATCH", vec)
		return 1
	}
	return 0
}

func main() {

	var found_xmas int

	matrix, err := input_to_matrix(os.Args[1])

	if err != nil {
		fmt.Println(err)
		return
	}

	for i, val := range matrix.Data {
		if val != "X" {
			continue
		}
		found := matrix.FindXmas(i)
		found_xmas += found

	}

	fmt.Println("Found XMAS:", found_xmas)

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
