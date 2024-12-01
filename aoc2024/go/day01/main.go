package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"
)

func main() {

	readFile, err := os.Open("input/day01")

	if err != nil {
		fmt.Println(err)
	}

	fileScanner := bufio.NewScanner(readFile)
	fileScanner.Split(bufio.ScanLines)

	var listOne []int
	var listTwo []int
	var listTwoCounter = make(map[int]int)

	for fileScanner.Scan() {
		row := strings.Fields(fileScanner.Text())
		listOne = append(listOne, strToInt(row[0]))
		listTwo = append(listTwo, strToInt(row[1]))
		listTwoCounter[strToInt(row[1])] += 1
	}

	readFile.Close()

	sort.Ints(listOne)
	sort.Ints(listTwo)

	var listDiff int = 0
	var simScore int = 0

	for i := range listOne {
		listDiff += int(math.Abs(float64(listOne[i] - listTwo[i]))) // there is no abc(int) function
		simScore += listOne[i] * listTwoCounter[listOne[i]]         // https://go.dev/blog/maps

	}

	fmt.Println(listDiff)
	fmt.Println(simScore)

}

func strToInt(input string) int {
	val, err := strconv.Atoi(input)

	if err != nil {
		panic(err)
	}

	return val
}
