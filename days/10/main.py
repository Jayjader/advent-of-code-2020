from collections import Counter
from itertools import pairwise, zip_longest, chain
from typing import TypeAlias

from graph import make_graph, paths_to_end, Edge

with open("./input") as file:
    problem_input = list(int(line) for line in file)

# bag of adapters
Adapter: TypeAlias = int
Bag: TypeAlias = set[Adapter, ...]


def make_bag(adapters: list[Adapter, ...]) -> Bag:
    # each adapter defined by its joltage rating, all unique
    bag: Bag = set(adapters)

    # socket / initial input is 0
    bag.add(0)

    # your device is rated for 3 + [highest rated adapter in bag]
    bag.add(max(bag) + 3)
    return bag


def part1(bag_: Bag) -> int:
    # we want the diffs for using *every device at once*
    # => just iterate pairwise over the sorted adapter ratings to get the diffs, then count them
    diffs = list(a2 - a1 for a1, a2 in pairwise(sorted(bag_)))
    count = Counter(diffs)

    # number of 1-jolt diffs * number of 3-jolt diffs
    return count[1] * count[3]


print(f"part 1: {part1(make_bag(problem_input))}")

# an arrangement is a sequence of adapters that successfully
# adapts from the socket (0) to your device (max(bag) + 3)
Arrangement: TypeAlias = tuple[Adapter, ...]
Rating: TypeAlias = int


def part2(bag_: Bag) -> int:
    # an adapter can accept input 0-3 jolts lower than its rating (and still *output* its rating)
    def accepts(adapter: Adapter) -> (Rating, Rating, Rating, Rating):
        return range(max(0, adapter - 3), adapter + 1)

    def can_accept(adapter: Adapter, rating: Rating) -> bool:
        return rating in accepts(adapter)

    assert can_accept(3, 3)
    assert can_accept(3, 0)
    assert can_accept(5, 3)
    assert not can_accept(3, 4)
    assert not can_accept(5, 1)
    assert not can_accept(8, 4)

    def successors(adapter: Adapter) -> range:
        return range(adapter + 1, adapter + 4)

    assert tuple(successors(0)) == (1, 2, 3)
    assert tuple(successors(5)) == (6, 7, 8)

    def bag_successors(adapter: Adapter):
        return set(successors(adapter)) & bag_

    bag_, temp = {0, 1, 2, 4}, bag_
    assert bag_successors(0) == {1, 2}
    assert bag_successors(1) == {2, 4}
    assert bag_successors(2) == {4}
    assert bag_successors(4) == set()
    bag_ = temp

    # to count arrangements, we need to build a graph where the vertices are the adapters and the directed edges the
    # acceptable connections <provider> -> <consumer> between them, then count the possible paths from the socket/output
    # to the device

    def edges_for_graph(adapter: int) -> list[Edge]:
        destinations = bag_successors(adapter)
        return list(zip_longest((adapter,) * len(destinations), destinations))

    edge_list = list(chain.from_iterable(edges_for_graph(adapter) for adapter in bag_))

    graph = make_graph(edge_list)

    bag_, temp = make_bag([16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]), bag_
    assert edges_for_graph(4) == [(4, 5), (4, 6), (4, 7)]
    assert edges_for_graph(1) == [(1, 4)]
    assert (
        paths_to_end(
            make_graph(
                list(chain.from_iterable(edges_for_graph(adapter) for adapter in bag_))
            )
        )
        == 8
    )
    bag_ = temp

    return paths_to_end(graph)


print(f"part 2: {part2(make_bag(problem_input))}")
