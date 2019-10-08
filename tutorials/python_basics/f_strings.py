# formatted string literals, f-strings

# %% fstrings
name = 'Eric'
age = 74

print(f'Hello, {name}, age {age}')
print(F'test {name}')


# %% expressions
print(f"{2 * 33}")

def to_lowercase(input):
    return input.lower()

print(f'{to_lowercase(name)} is funny')
print(f'{name.lower()}')


# %% class
class Comedian:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def __str__(self):
        return f"{self.first_name} {self.last_name} is {self.age}."

    def __repr__(self):
        return f"{self.first_name} {self.last_name} is {self.age}. Surprise!"

new_comedian = Comedian("Eric", "Srerik", "75")

print(f'{new_comedian}')
print(f'{new_comedian!r}')


# %% multiline

name = "Eric"
profession = "comedian"
affiliation = "Monty Python"

m = (
    f"Hi {name}",
    f"bla {profession}",
    f"eee {affiliation}"
)
print(m)

m = f"""
Hi {name}.
You are {profession}
E {affiliation}.
"""
m

# %% others
# f string is fast (faster then % and .format())

print(f"{{77}}")
print(f"{{{77}}}")
print(f"{{{{77}}}}")
