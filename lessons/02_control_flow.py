"""
Lesson 02: Control flow

Goal: write branches and loops the Pythonic way, including structural pattern matching.
"""

# 1. CONCEPT
# Blocks are defined by indentation (4 spaces), not braces. Conditions need no parentheses.
#
#   if / elif / else          -> branching (there is also the one-line `a if cond else b`)
#   for x in iterable         -> iterate over *any* iterable; there is no C-style for(;;)
#   while cond                -> loop on a condition
#   break / continue          -> as in C#; loops also accept an `else:` clause (runs if no break)
#   match / case (3.10+)      -> structural pattern matching, much richer than a C# switch

# 2. EXAMPLES


def demo_branches_and_loops() -> None:
    temperature = 31
    label = "hot" if temperature > 30 else "ok"  # conditional expression
    print("label:", label)

    if 0 < temperature < 40:  # chained comparison
        print("in range")

    for i in range(3):  # range(stop) / range(start, stop, step), stop is exclusive
        print("i =", i, end="; ")
    print()

    for index, letter in enumerate("abc", start=1):
        print(index, letter, end="; ")
    print()

    for n in range(2, 10):
        for divisor in range(2, n):
            if n % divisor == 0:
                break
        else:  # no break happened -> n is prime
            print(f"{n} is prime")


def describe(command: object) -> str:
    match command:
        case "quit" | "exit":  # OR-pattern
            return "leaving"
        case ["go", direction]:  # sequence pattern, captures `direction`
            return f"going {direction}"
        case {"type": "move", "dx": dx, "dy": dy}:  # mapping pattern
            return f"moving by ({dx}, {dy})"
        case int(n) if n < 0:  # class pattern + guard
            return "negative number"
        case int() | float():
            return "number"
        case None:
            return "nothing"
        case _:  # wildcard, like `default:`
            return "unknown"


def demo_match() -> None:
    for sample in (
        "exit",
        ["go", "north"],
        {"type": "move", "dx": 1, "dy": 2},
        -5,
        3.14,
        None,
        b"x",
    ):
        print(f"{sample!r:>40} -> {describe(sample)}")


def demo_while() -> None:
    n, steps = 27, 0
    while n != 1:  # Collatz sequence
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    print("Collatz steps for 27:", steps)


# 3. C# EQUIVALENT
#
#   Python                          C#
#   ------------------------------  -------------------------------------
#   for x in items:                 foreach (var x in items)
#   for i in range(n):              for (int i = 0; i < n; i++)
#   for i, x in enumerate(items):   items.Select((x, i) => ...)
#   a if cond else b               cond ? a : b
#   match/case                      switch expression + property/list patterns
#   while / break / continue        same
#   and / or / not                  && / || / !

# 4. COMMON PITFALLS
#
#   a) `range(5)` stops at 4. The end value is always exclusive.
#   b) Python has no `++`. Write `i += 1`.
#   c) In `match`, a bare name is a *capture*, not a comparison:
#        case x:   matches anything and binds x.   Use a literal or a dotted name to compare.
#   d) Never mutate a list while iterating over it; iterate over a copy or build a new list.

# 5. EXERCISE
# Open exercises/ex02_control_flow.py, implement the functions, then run:
#     python runner.py test 02

if __name__ == "__main__":
    demo_branches_and_loops()
    print()
    demo_match()
    print()
    demo_while()
