package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
)

func main() {

	re, err := regexp.Compile(`^mul\((\d+),(\d+)\)`) // to raw string ` instead "  https://go.dev/ref/spec#String_literals
	if err != nil {
		panic(err)
	}

	readFile, err := os.Open("input/day03-full")

	if err != nil {
		fmt.Println(err)
	}

	fileScanner := bufio.NewScanner(readFile)
	fileScanner.Split(bufio.ScanLines)

	var result int = 0
	var enabler bool = true

	for fileScanner.Scan() {

		row := string(fileScanner.Text())
		var pos int = 0

		for pos < len(row)-3 {
			fmt.Println(pos)
			// fmt.Printf("%c", row[pos])  How to print char from string (without that prints ascii number?

			if pos <= len(row)-4 && row[pos:pos+4] == "do()" {
				enabler = true
				pos += 3
				continue
			}

			if pos < len(row)-7 && row[pos:pos+7] == "don't()" {
				enabler = false
				pos += 6
				continue
			}

			if row[pos:pos+3] == "mul" && enabler {
				matches := re.FindStringSubmatch(row[pos:])

				if len(matches) > 1 {

					var res_mult int = strToInt(matches[1]) * strToInt(matches[2])
					fmt.Println(matches[0], res_mult)

					result += res_mult

					pos += len(matches[0])

					continue
				}

			}

			pos++
		}

	}

	readFile.Close()

	fmt.Println(result)

}

func strToInt(input string) int {
	val, err := strconv.Atoi(input)

	if err != nil {
		panic(err)
	}

	return val
}
