from itertools import combinations, chain


def is_valid(preamble, n):
    pairs = set(combinations(preamble, 2))
    sums = set(sum(pair) for pair in pairs)
    equal = set(s == n for s in sums)
    return any(equal)


TEST_PREAMBLE = list(range(1, 26))

assert is_valid(TEST_PREAMBLE, 26)
assert is_valid(TEST_PREAMBLE, 49)
assert not is_valid(TEST_PREAMBLE, 100)
assert not is_valid(TEST_PREAMBLE, 50)

TEST_PREAMBLE = list(chain(range(1, 20), range(21, 26), (45,)))

assert is_valid(TEST_PREAMBLE, 26)
assert not is_valid(TEST_PREAMBLE, 65)
assert is_valid(TEST_PREAMBLE, 64)
assert is_valid(TEST_PREAMBLE, 66)

with open("./input") as input_file:
    numbers = list(int(line) for line in input_file)

preamble = numbers[:25]

for number in numbers[25:]:
    if not is_valid(preamble, number):
        print(f"first invalid number: {number}")
        first_invalid = number
        break
    preamble = [*preamble[1:], number]


def nwise(collection, n):
    size = len(collection)
    for i in range(0, size - n):
        yield collection[i : (i + n)]


summing_tuple = ()
# for n in range(len(numbers)):
for n in range(2, len(numbers) // 2):
    for tuple_ in nwise(numbers, n):
        # print(f"tuple: {tuple_}")
        if sum(tuple_) == first_invalid:
            print(f"summing tuple: {tuple_}")
            summing_tuple = tuple_
            break

if len(summing_tuple) > 0:
    smallest = min(summing_tuple)
    largest = max(summing_tuple)
    print(f"smallest: {smallest}, largest: {largest}")
    print(f"sum: {smallest + largest}")
