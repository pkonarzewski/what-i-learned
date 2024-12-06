package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {

	readFile, err := os.Open("input/day03-test")

	if err != nil {
		fmt.Println(err)
	}

	fileScanner := bufio.NewScanner(readFile)
	fileScanner.Split(bufio.ScanLines)

	for fileScanner.Scan() {
		row := strings.Fields(fileScanner.Text())
		fmt.Println(row)
	}

	readFile.Close()

}

func strToInt(input string) int {
	val, err := strconv.Atoi(input)

	if err != nil {
		panic(err)
	}

	return val
}
