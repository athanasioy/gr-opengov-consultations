# functions that contain the "yield" keyword do not simply return the value after the yield.
# they return a generator object that can be iterated against.

# generator objects have a "state", meaning that they remember where they last stopped
# when iterated inside a for loop.

# for example

def gen():
    yield "this is first"
    yield "this is second"
    yield "final third"

myGen = gen()
for i in myGen:
    print(i)
    # prints all three texts 

# you can create generators in many ways
# for example


def odd_nums(limit:int):
    # generate odd numbers
    n = range(limit)
    for i in n:
        if (i%2==1):
            yield i

mygen = odd_nums(23)

for i in mygen:
    print(f"mygen first try {i}")

# Note that once a generator has been used, it is not accesible again

for i in mygen:
    print(f"mygen second try {i}") # nothing

