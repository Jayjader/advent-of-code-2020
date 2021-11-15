from collections import namedtuple, Counter
from enum import Enum
from itertools import chain
from typing import Literal, TypeAlias, NamedTuple

import pytest


class GridCell(Enum):
    FLOOR = "."
    EMPTY_SEAT = "L"
    OCCUPIED_SEAT = "#"


class Position(NamedTuple):
    x: int
    y: int


Grid: TypeAlias = dict[Position, GridCell]


def parse_problem_input(file_):
    return {
        Position(x, y): GridCell(square)
        for y, line in enumerate(file_)
        for x, square in enumerate(line.strip())
    }


with open("./input") as file:
    problem_grid = parse_problem_input(file)


def occupied(cell: GridCell) -> bool:
    return cell == GridCell.OCCUPIED_SEAT


def neighbours(position: Position, grid: Grid) -> tuple[GridCell, ...]:
    x, y = position
    return tuple(
        filter(
            lambda cell: cell is not None,
            (
                grid.get(Position(x + dx, y + dy))
                for dx, dy in (
                    (-1, -1),
                    (0, -1),
                    (1, -1),
                    (1, 0),
                    (1, 1),
                    (0, 1),
                    (-1, 0),
                )
            ),
        )
    )


@pytest.mark.parametrize("position,expected_neighbours")
def test_neighbours(position, expected_neighbours):
    grid = parse_problem_input("""LL.
            L..""")
    assert neighbours(position, grid) == expected_neighbours

@pytest.mark.parametrize(
    "input_g,expected_g",
    [
        ("..\n..\n", "..\n..\n"),
        ("L.\n..", "#.\n.."),
        ("""LL.
            L..""",
         """##.
            #.."""),
        ("""##.
            #.#""",
         """#L.
            #.#"""),
    ],
)
def test_update(input_g, expected_g):
    grid = parse_problem_input(input_g)
    expected_grid_after_update = parse_problem_input(expected_g)

    assert update_grid(grid) == expected_grid_after_update


def update_seat(position: Position, grid: Grid) -> GridCell:
    # pass  # this is for quick commenting/uncommenting the function body while allowing the program to typecheck as black doesn't yet understand match cases
    match grid[position], sum(map(occupied, neighbours(position, grid))):
        case GridCell.EMPTY_SEAT, 0:
            return GridCell.OCCUPIED_SEAT
        case GridCell.OCCUPIED_SEAT, n if n >= 4:
            return GridCell.EMPTY_SEAT
        case _cell, _:
            return _cell


def reppr(grid: Grid) -> str:
    size = max(y for _x, y in grid)
    return "\n".join(
        "".join(grid[Position(x, y)].value for x in range(size)) for y in range(size)
    )


def update_grid(grid: Grid) -> Grid:
    return {position: update_seat(position, grid) for position in grid}


def test_grid_update():
    test_grid = parse_problem_input(
        """L.LL.LL.LL
    LLLLLLL.LL
    L.L.L..L..
    LLLL.LL.LL
    L.LL.LL.LL
    L.LLLLL.LL
    ..L.L.....
    LLLLLLLLLL
    L.LLLLLL.L
    L.LLLLL.LL
    """
    )

    step_1 = update_grid(test_grid)
    assert step_1 == parse_problem_input(
        """#.##.##.##
    #######.##
    #.#.#..#..
    ####.##.##
    #.##.##.##
    #.#####.##
    ..#.#.....
    ##########
    #.######.#
    #.#####.##
    """
    )
    step_2 = update_grid(step_1)
    # print(reppr(step_2))
    expected_step_2 = parse_problem_input(
        """#.LL.L#.##
    #LLLLLL.L#
    L.L.L..L..
    #LLL.LL.L#
    #.LL.LL.LL
    #.LLLL#.##
    ..L.L.....
    #LLLLLLLL#
    #.LLLLLL.L
    #.#LLLL.##
    """
    )
    diff = set(step_2.items()) | set(expected_step_2.items()) - (
        set(step_2.items()) & set(expected_step_2.items())
    )
    dict_diff: dict[Position, list[GridCell]] = dict()
    for d in diff:
        position, cell = d
        dict_diff.setdefault(position, []).append(cell)
    # print(dict_diff)
    # print(
    #     Counter(
    #         chain.from_iterable(
    #             (position,) * len(cells) for position, cells in dict_diff.items()
    #         )
    #     )
    # )
    assert step_2 == expected_step_2
    step_3 = update_grid(step_2)
    assert step_3 == parse_problem_input(
        """#.##.L#.##
    #L###LL.L#
    L.#.#..#..
    #L##.##.L#
    #.##.LL.LL
    #.###L#.##
    ..#.#.....
    #L######L#
    #.LL###L.L
    #.#L###.##
    """
    )
    step_4 = update_grid(step_3)
    assert step_4 == parse_problem_input(
        """#.#L.L#.##
    #LLL#LL.L#
    L.L.L..#..
    #LLL.##.L#
    #.LL.LL.LL
    #.LL#L#.##
    ..L.L.....
    #L#LLLL#L#
    #.LLLLLL.L
    #.#L#L#.##
    """
    )
    step_5 = update_grid(step_4)
    assert step_5 == parse_problem_input(
        """#.#L.L#.##
    #LLL#LL.L#
    L.#.L..#..
    #L##.##.L#
    #.#L.LL.LL
    #.#L#L#.##
    ..L.L.....
    #L#L##L#L#
    #.LLLLLL.L
    #.#L#L#.##
    """
    )


def part1(starting_grid: Grid) -> int:
    past_step: Grid = starting_grid
    current_step: Grid = update_grid(past_step)
    steps = 1
    while past_step != current_step:
        past_step = current_step
        current_step = update_grid(past_step)
        steps += 1
    return steps


print(f"part 1: {part1(problem_grid)}")
