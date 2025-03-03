package main

import "fmt"

func main() {

	for_loop()

}

func for_loop() {
	for i := 1; i <= 10; i++ {
		if i%2 == 0 {
			fmt.Print("e:")
		} else if i == 5 {
			fmt.Print("nice:")

		} else {
			fmt.Print("o:")
		}

		fmt.Println(i)

	}

	switch_st(1)
}

func switch_st(i int) {
	switch i {
	case 0:
		fmt.Println("zero")
	case 1:
		fmt.Println("one")
	default:
		fmt.Println("EEE")
	}
}
