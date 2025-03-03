package main

import "fmt"

func main() {
	var x string
	const eee string = "ABC" // const
	x = "Hello"

	fmt.Println(x)

	y := "abc" // no type, compiler infer type based on the literal value

	fmt.Println(y)

	fmt.Println(eee)

	// multi variables
	var ( // or const
		a = 2
		b = 3
		c = 5
	)
	fmt.Println(a + b + c)

	input_test()

}

func input_test() {
	fmt.Print("Enter number: ")
	var input float64
	fmt.Scanf("%f", &input)

	output := input * 2

	fmt.Println(output)
}
