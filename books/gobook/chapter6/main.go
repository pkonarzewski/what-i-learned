package main

import "fmt"

func main() {

	x := [5]float64{1, 2, 3, 4, 5}

	var total float64 = 0
	for _, value := range x {
		total += value
	}
	fmt.Println(total / float64(len(x)))

	slice_test()
}

func slice_test() {

	x := [5]float64{1, 2, 3, 4, 5}

	var s1 []float64
	s2 := make([]float64, 3)

	fmt.Println(x, s1, s2)
	fmt.Println(x[:3])

	s3 := []int{1, 2, 3}
	s4 := append(s3, 6, 6, 6)

	fmt.Println(s3, s4, append(s4, 1))

	s5 := []int{-9, -9}
	copy(s5, s3)

	fmt.Println(s5)

	map_test()

}

func map_test() {

	x := make(map[string]int)
	x["test"] = 10

	fmt.Println(x["test"])

	name, ok := x["eee"]
	fmt.Println(name, ok)

	if name, ok := x["eee"]; ok {
		fmt.Println("found", name)
	}

	elements := map[string]string{
		"abc": "EEE",
	}

	fmt.Println(elements)

}
