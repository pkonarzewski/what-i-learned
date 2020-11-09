is_fizz = lambda x: x % 3 == 0
is_buzz = lambda x: x % 5 == 0

for n in range(100):
    print(n, end=" ")
    if is_fizz(n):
        print("Fizz", end=" ")
    if is_buzz(n):
        print("Buzz", end=" ")

    print("")
