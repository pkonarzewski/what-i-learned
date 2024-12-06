package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

func validateResult(input []string, threshold int) int {
	// No default value in func
	// can use struct instea d https://stackoverflow.com/a/13603885
	var inc bool = input[1] > input[0]
	var errCnt int = 0

	for i := 0; i < len(input)-1; i++ {
		var diff int = strToInt(input[i+1]) - strToInt(input[i])

		if (inc == true && diff <= 0) || (inc == false && diff >= 0) {
			errCnt++
		}

		if int(math.Abs(float64(diff))) > 3 {
			errCnt++
		}

	}

	if errCnt <= threshold {
		return 1
	}

	return 0
}

func main() {

	readFile, err := os.Open("input/day02-test")

	if err != nil {
		fmt.Println(err)
	}

	fileScanner := bufio.NewScanner(readFile)
	fileScanner.Split(bufio.ScanLines)

	var validCnt int = 0

	for fileScanner.Scan() {
		row := strings.Fields(fileScanner.Text())
		validCnt += validateResult(row, 1)

	}

	readFile.Close()

	fmt.Println(validCnt)

}

func strToInt(input string) int {
	val, err := strconv.Atoi(input)

	if err != nil {
		panic(err)
	}

	return val
}
