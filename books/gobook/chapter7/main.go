package main

import "fmt"

func main() {
	vals := []float64{1, 2, 3}
	res := average(vals)

	fmt.Println(res)

	fmt.Println(test_sum(1, 2))

	xs := []int{1, 2, 3}

	fmt.Println(test_sum(xs...))

	test_closure()

	nextEven := makeEvenGenerator()
	fmt.Println(nextEven())
	fmt.Println(nextEven())
	fmt.Println(nextEven())

	fmt.Println(factorial(5))

	defer second()
	first()

	panic_example()
}

func average(xs []float64) float64 {
	total := 0.0
	for _, v := range xs {
		total += v
	}
	return total / float64(len(xs))
}

func test_sum(args ...int) int {
	total := 0
	for _, v := range args {
		total += v
	}
	return total
}

func test_closure() {
	z := 5
	add := func(x, y int) int { // if same of parameters than type only one
		return x + y + z
	}
	fmt.Println(add(1, 1))
}

func makeEvenGenerator() func() uint {
	i := uint(0)
	return func() (ret uint) {
		ret = i
		i += 2
		return
	}
}

func factorial(x uint) uint {
	if x == 0 {
		return 1
	}

	return x * factorial(x-1)
}

func first() {
	fmt.Println("1st")
}

func second() {
	fmt.Println("2nd")
}

func panic_example() {
	defer func() {
		str := recover()
		fmt.Println(str)
	}()
	panic("PANIC")
}
