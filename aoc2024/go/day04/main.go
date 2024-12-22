package main

import (
	"bufio"
	"fmt"
	"os"
	"slices"
)

const XMAS = "XMAS"
const MAS = "MAS"

func load(inputName string) ([]string, int, error) {
	var input []string
	var row_len int

	readFile, err := os.Open("input/" + inputName)
	defer readFile.Close()

	if err != nil {
		return nil, 0, err
	}

	fileScanner := bufio.NewScanner(readFile)
	fileScanner.Split(bufio.ScanLines)

	for fileScanner.Scan() {
		row := fileScanner.Text()
		row_len = len(row)

		for _, char := range row {
			input = append(input, string(char))
		}

	}
	return input, row_len, nil
}

func find_xmas(input []string, row_len int) {
	found_xmas := 0
	var found_vectors [][4]int
	for i := 0; i < len(input); i++ {
		if input[i] != "X" {
			continue
		}

		for drow := -1; drow <= 1; drow++ {
			for dcol := -1; dcol <= 1; dcol++ {

				if i+3*dcol+3*drow*row_len < 0 || i+3*dcol+3*drow*row_len > len(input)-1 {
					continue
				}

				if (i+3*dcol)/row_len != i/row_len {
					// spil over to next line
					continue
				}

				found_str := ""

				var vector [4]int
				for n := 0; n < 4; n++ {
					found_str += input[i+n*dcol+n*drow*row_len]
					vector[n] = i + n*dcol + n*drow*row_len
				}

				if found_str == XMAS {
					// fmt.Println(i, vector)
					found_xmas++

					if slices.Contains(found_vectors, vector) {
						panic("Duplicate")
					}

					found_vectors = append(found_vectors, vector)

				}
			}
		}

	}

	fmt.Println(found_xmas)
}

func findMasX(input []string, row_len int) {
	answer := 0

	for i := row_len - 1; i < len(input)-row_len; i++ {
		found := ""

		if input[i] != "A" {
			continue
		}

		if i%row_len == 0 || i%row_len == row_len-1 {
			fmt.Println(i)
			continue
		}

		for drow := -1; drow <= 1; drow += 2 {
			for dcol := -1; dcol <= 1; dcol += 2 {
				found += input[i+drow*row_len+dcol]
			}
		}

		if found == "MMSS" || found == "MSMS" || found == "SSMM" || found == "SMSM" {
			answer++
		}

	}

	fmt.Println("Found MAS-X:", answer)
}

func main() {

	input, row_len, err := load(os.Args[1])

	if err != nil {
		fmt.Println(err)
		return

	}

	find_xmas(input, row_len)
	// findMasX(input, row_len)

}
