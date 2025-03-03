package main

import "fmt"

func main() {
	fmt.Println("1 + 1 =", 1+1)
	fmt.Println("1 + 1 =", 1.0+1.0) // no space between operator and operands

	fmt.Println("1\n1", `2\n3`)         //  backtick for string literal
	fmt.Println(len("asdf"), "EEEE"[0]) //  characters are represented by byte

	// string literal, result of expression (numeric literal, operator, another literal)
}
