from __future__ import annotations
from typing import Literal, TypeAlias, Iterable

Dead: TypeAlias = Literal["."]
Alive: TypeAlias = Literal["#"]
Cell: TypeAlias = Alive | Dead


def parse_input(lines: Iterable[str]) -> tuple[tuple[Cell, ...], ...]:
    return tuple(
        tuple(character for character in line if character in (".", "#"))
        for line in lines
    )


with open("./input") as file:
    problem_input = parse_input(file)
    for row in problem_input:
        print(row)


