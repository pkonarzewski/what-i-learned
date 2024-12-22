package main

import (
	"bufio"
	"fmt"
	"os"
	"slices"
	"strconv"
	"strings"
)

func load(inputName string) ([][]int, [][]int, error) {
	var pageOrder [][]int
	var pages [][]int

	readFile, err := os.Open("input/" + inputName)
	defer readFile.Close()

	if err != nil {
		return nil, nil, err
	}

	fileScanner := bufio.NewScanner(readFile)
	fileScanner.Split(bufio.ScanLines)

	foundSpaceInFile := false

	for fileScanner.Scan() {
		row := fileScanner.Text()

		if row == "" {
			foundSpaceInFile = true
			continue
		}

		if !foundSpaceInFile {
			row_els := strings.Split(row, "|")
			pageOrder = append(pageOrder, ArrayStrToInt(row_els))
		} else {
			row_els := strings.Split(row, ",")
			pages = append(pages, ArrayStrToInt(row_els))
		}
	}

	return pageOrder, pages, nil

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

func createManualMap(input [][]int) map[int][]int {
	manualMap := make(map[int][]int)

	for _, val := range input {
		manualMap[val[0]] = append(manualMap[val[0]], val[1])
	}

	return manualMap
}

func isCorrect(pageMap map[int][]int, pages []int) bool {
	for i := 0; i < len(pages)-1; i++ {
		node := pageMap[pages[i]]

		for _, val := range pages[i+1:] {
			if !slices.Contains(node, val) {
				return false
			}
		}

	}
	return true
}

func fixOrder(pageMap map[int][]int, pages []int) []int {
	fmt.Println("===", pages)

	i := 0
	for i < len(pages)-1 { // while loop in Go

		posVal := pages[i]
		node := pageMap[posVal]

		fmt.Println(posVal, node)

		for _, val := range pages[i+1:] {
			if !slices.Contains(node, val) {
				fmt.Println("<>", posVal)

				pages = append(pages[:i], pages[i+1:]...)
				pages = append(pages, posVal)
				// fmt.Println(fixed)

				i--
				break
			}
		}

		i++

	}
	fmt.Println(">", pages)
	return pages
}

func main() {
	correctAnswer := 0
	fixedAnswer := 0
	pageOrder, pagesSets, err := load(os.Args[1])

	if err != nil {
		fmt.Println(err)
		return
	}

	orderMap := createManualMap(pageOrder)

	for _, page := range pagesSets {
		// fmt.Println("Check pages:", page)
		if isCorrect(orderMap, page) {
			correctAnswer += page[len(page)/2]
		} else {
			page = fixOrder(orderMap, page)
			fixedAnswer += page[len(page)/2]
		}
	}

	fmt.Println("Answer 1:", correctAnswer)
	fmt.Println("Answer 2:", fixedAnswer)
}
