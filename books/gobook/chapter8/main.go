package main

import "fmt"

func zero(x *float64) {
	*x = *x * *x
}

func main() {
	x := 2.0
	zero(&x)
	fmt.Println(x)
}
