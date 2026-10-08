"""
Lesson 03: Functions

Goal: use Python's flexible argument system, closures and lambdas, and avoid the
mutable-default-argument trap.
"""

# 1. CONCEPT
# Functions are first-class objects: you can pass them around, store them, return them.
#
#   def f(a, b=2, *args, key, **kwargs)
#        |  |     |      |    '-- extra keyword arguments collected into a dict
#        |  |     |      '------ keyword-only (everything after *args / a bare *)
#        |  |     '------------- extra positional arguments collected into a tuple
#        |  '------------------- default value (evaluated ONCE, at definition time)
#        '---------------------- positional-or-keyword
#
# Functions return None unless they `return` something. Returning several values really
# returns one tuple, which the caller unpacks.

from collections.abc import Callable

# 2. EXAMPLES


def greet(name: str, greeting: str = "Hello", *, shout: bool = False) -> str:
    message = f"{greeting}, {name}!"
    return message.upper() if shout else message


def total(*numbers: float) -> float:
    return sum(numbers)  # numbers is a tuple


def describe(**attributes: object) -> str:
    return ", ".join(f"{key}={value}" for key, value in attributes.items())  # attributes is a dict


def min_max(values: list[int]) -> tuple[int, int]:
    return min(values), max(values)  # "multiple return values" = one tuple


def make_multiplier(factor: int) -> Callable[[int], int]:
    def multiply(x: int) -> int:  # closure: captures `factor` from the enclosing scope
        return x * factor

    return multiply


def make_counter() -> Callable[[], int]:
    count = 0

    def increment() -> int:
        nonlocal count  # without `nonlocal`, `count += 1` would create a new local
        count += 1
        return count

    return increment


def demo() -> None:
    print(greet("Ana"), "|", greet("Ana", "Hi", shout=True), "|", greet(greeting="Yo", name="Bo"))
    print(total(1, 2, 3), "|", describe(a=1, b="two"))
    low, high = min_max([4, 8, 1])  # tuple unpacking
    print("min/max:", low, high)

    values = [1, 2, 3]
    print("unpack call:", total(*values), "|", describe(**{"x": 1, "y": 2}))

    triple = make_multiplier(3)
    print("triple(5):", triple(5))
    counter = make_counter()
    print("counter:", counter(), counter(), counter())

    words = ["banana", "kiwi", "apple"]
    print(sorted(words, key=lambda w: len(w)))  # lambda = tiny anonymous function


# The mutable-default trap ----------------------------------------------------------------


def buggy_append(item: int, bucket: list[int] = []) -> list[int]:
    bucket.append(item)  # the SAME list object is reused on every call!
    return bucket


def fixed_append(item: int, bucket: list[int] | None = None) -> list[int]:
    if bucket is None:  # idiom: use None as the sentinel, create the list inside
        bucket = []
    bucket.append(item)
    return bucket


def demo_default_trap() -> None:
    print("buggy:", buggy_append(1), buggy_append(2), buggy_append(3))  # [1, 2, 3] x3 (shared!)
    print("fixed:", fixed_append(1), fixed_append(2), fixed_append(3))


# 3. C# EQUIVALENT
#
#   Python                          C#
#   ------------------------------  ---------------------------------------------
#   def f(a, b=2)                   void F(int a, int b = 2)        (defaults are compile-time consts)
#   f(b=1, a=0)                     F(b: 1, a: 0)                   (named arguments)
#   *args                           params object[] args
#   **kwargs                        no direct equivalent (Dictionary<string, object>)
#   return a, b                     return (a, b);                   (ValueTuple)
#   lambda x: x * 2                 x => x * 2
#   Callable[[int], int]            Func<int, int>
#   closure + nonlocal              captured variable in a lambda / local function

# 4. COMMON PITFALLS
#
#   a) Mutable default arguments (list, dict, set) are shared between calls. Use None.
#   b) Assigning to a captured variable needs `nonlocal`; reading it does not.
#   c) Positional args after keyword args are a SyntaxError: f(a=1, 2).
#   d) A function with no `return` gives None, so `x = my_list.sort()` sets x to None.

# 5. EXERCISE
# Open exercises/ex03_functions.py, implement the functions, then run:
#     python runner.py test 03
# From this lesson on, the tests use pytest.mark.parametrize: open one and see how it works.

if __name__ == "__main__":
    demo()
    print()
    demo_default_trap()
