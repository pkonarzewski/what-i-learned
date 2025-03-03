# Go book

## 9. Structs and Interfaces

### Structs

Structs - is a composite data type that groups together variables (fields). Similiar to classes in OOP but don't support inheritance.

type Circle struct {
  x flaot64
  y float64
  r float64
}

or

type Circle struct {x,y,r float64}

initialization

var c Circle

c := new(Circle) allocates memory for all the fields, sets them to zero and returns pointer

> default values for empty (0 ints, 0.0 floats, "" strings, nil pointers)


c := Circle{x: 0, y:0, r:5}
c := Circle{0,0,5}

#### Fields access with . operator

c.x  =10
c.y = 5

> arguments are always copied

#### Methods

methods - special type of function

func (c *Circle) area() float64 {
  return math.Pi * c.r * c.r
}

c.area()

#### Embeded types

Embeded types (stuct embedding) - way to compose types including one type insdie another. Composition over inheritance.

is anonymouse field

type Android struct {
  Person
  Model string
}

// Android is a person

a := new(Android)
a.Talk()

#### Interfaces

interface - is a type that defines a set of method signatures. Implements interface if it provides implementations for all the methods dacleread in interface.

type Shape interface {
  area() flaot64
}

we define method set. list of methods that a type must have in order to implement interface.

func totalArea(shapes ...Shape) foat64 {
  for shapes {s.area()}
}

totalArea(&c, &r)

interfaces used as fields

type MultiShape sturct {
  shapes []Shape
}
