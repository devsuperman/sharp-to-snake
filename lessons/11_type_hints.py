"""
Lesson 11: Type hints

Goal: annotate Python code so tools (mypy, your editor) can catch bugs the way the C#
compiler does, without changing runtime behaviour.
"""

# 1. CONCEPT
# Annotations are *hints*: Python itself ignores them at runtime. A separate checker,
# `mypy` (or pyright), reads them and reports mismatches before you run the code.
#
#   def f(x: int, name: str = "a") -> bool        parameters and return type
#   list[int], dict[str, float], tuple[int, str]  built-in generics (3.9+)
#   tuple[int, ...]                               tuple of any length
#   int | None                                    union / optional (3.10+; replaces Optional[int])
#   Callable[[int], str]                          function type (from collections.abc)
#   Iterable[T], Sequence[T], Mapping[K, V]       prefer abstract types for PARAMETERS
#   TypedDict                                     a dict with a fixed set of typed keys
#   Protocol                                      structural typing: "anything with these methods"
#   def f[T](x: T) -> T                           generics with the 3.12 syntax
#   Final, Literal, NewType                       constants, exact values, distinct aliases
#
# Run the checker:   mypy --strict lessons/11_type_hints.py

from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Literal, NotRequired, Protocol, TypedDict

# 2. EXAMPLES


def average(values: Iterable[float]) -> float:
    items = list(values)
    return sum(items) / len(items)


def find_user(users: Mapping[int, str], user_id: int) -> str | None:
    return users.get(user_id)  # mypy forces callers to handle the None case


def first[T](items: Sequence[T]) -> T | None:  # generic function, PEP 695 syntax (3.12+)
    return items[0] if items else None


def apply_twice(func: Callable[[int], int], value: int) -> int:
    return func(func(value))


class Address(TypedDict):
    city: str
    zip_code: NotRequired[str]  # optional key


class Greeter(Protocol):  # structural: no inheritance needed, like Go interfaces
    def greet(self) -> str: ...


@dataclass
class English:
    def greet(self) -> str:
        return "Hello"


@dataclass
class Portuguese:
    def greet(self) -> str:
        return "Olá"


def welcome(greeters: Iterable[Greeter]) -> list[str]:
    return [g.greet() for g in greeters]  # English and Portuguese both satisfy Greeter


type Direction = Literal["north", "south", "east", "west"]  # type alias (3.12+)


OPPOSITE: dict[Direction, Direction] = {
    "north": "south",
    "south": "north",
    "east": "west",
    "west": "east",
}


def turn_around(direction: Direction) -> Direction:
    return OPPOSITE[direction]


def demo() -> None:
    print(average([1, 2, 3.5]), find_user({1: "Ana"}, 2), first(["x", "y"]), first([]))
    print(apply_twice(lambda n: n * 3, 2))
    address: Address = {"city": "Lisbon"}
    print(address, "| required keys:", sorted(Address.__required_keys__))
    print(welcome([English(), Portuguese()]), turn_around("north"))
    # Nothing is enforced at runtime: `welcome(["oops"])` would only fail when it runs,
    # while mypy rejects it before. Try it: add that call and run mypy --strict.


# 3. C# EQUIVALENT
#
#   Python                          C#
#   ------------------------------  ----------------------------------------------
#   x: int                          int x
#   str | None                      string?  (nullable reference types)
#   list[int]                       List<int> / IReadOnlyList<int>
#   Iterable[T], Sequence[T]        IEnumerable<T>, IReadOnlyList<T>
#   Mapping[K, V]                   IReadOnlyDictionary<K, V>
#   def first[T](xs: Sequence[T])   T? First<T>(IReadOnlyList<T> xs)
#   Callable[[int], str]            Func<int, string>
#   Protocol                        interface (but satisfied implicitly, structurally)
#   TypedDict                       record / DTO with a fixed shape
#   Literal["a", "b"]               enum (lightweight)
#   mypy                            the compiler + nullable analysis (but opt-in and external)
#   Any                             dynamic / object

# 4. COMMON PITFALLS
#
#   a) Hints are not enforced at runtime. Validate external input explicitly.
#   b) Annotate parameters with abstract types (Iterable, Mapping) and return concrete ones (list, dict).
#   c) `list` of subtype is not a `list` of base type (invariance); use Sequence for read-only.
#   d) Overusing `Any` silently turns checking off. Prefer `object` or a Protocol.
#   e) Install and run mypy; hints nobody checks drift out of date.

# 5. EXERCISE
# Open exercises/ex11_type_hints.py, implement and ANNOTATE everything, then run:
#     python runner.py test 11
# One test runs `mypy --strict` on your file, so the annotations must be complete and correct.

if __name__ == "__main__":
    demo()
