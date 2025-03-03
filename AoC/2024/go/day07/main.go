package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

const ADD = 0
const MULT = 1
const CONCAT = 2

type Input struct {
	expResult int
	elements  []int
}

func strToInt(input string) int {
	val, err := strconv.Atoi(input)

	if err != nil {
		panic(err)
	}

	return val
}

func IntToString(input int) string {
	return strconv.Itoa(input)
}

func ArrayStrToInt(input []string) []int {
	var output []int

	for _, val := range input {
		val, err := strconv.Atoi(val)

		if err != nil {
			panic(err)
		}
		output = append(output, val)

	}

	return output
}

func readCalibrations(filename string) (<-chan string, <-chan error) {
	lines := make(chan string)
	errors := make(chan error, 1)

	go func() {
		defer close(lines)
		defer close(errors)

		file, err := os.Open(filename)
		if err != nil {
			errors <- err
			return
		}
		defer file.Close()

		scanner := bufio.NewScanner(file)
		for scanner.Scan() {
			lines <- scanner.Text()
		}

		if err := scanner.Err(); err != nil {
			errors <- err
		}
	}()

	return lines, errors
}

func rec(i int, sum int, target int, line []int) int {
	fmt.Println(sum)
	if i == len(line)-1 {
		fmt.Println(sum)
		if sum == target {
			return target
		}
		return 0
	}

	return rec(i+1, sum+line[i], target, line)

}

func parseCalib(line string) Input {
	res := strings.Split(line, ":")
	expInt := strToInt(res[0])
	elements := ArrayStrToInt(strings.Split(strings.Trim(res[1], " "), " "))
	return Input{expInt, elements}
}

func main() {
	var result1 int
	var result2 int

	lines, errors := readCalibrations(os.Args[1])

	for line := range lines {
		input := parseCalib(line)

		fmt.Println(input)
		result1 += rec(0, input.elements[0], input.expResult, input.elements)

	}

	fmt.Println("Results 1:", result1)
	fmt.Println("Results 2:", result2)

	if err := <-errors; err != nil {
		fmt.Printf("Error reading file: %v\n", err)
	}

}
