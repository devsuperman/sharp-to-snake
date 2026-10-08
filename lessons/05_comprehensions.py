"""
Lesson 05: Comprehensions and iteration

Goal: transform data declaratively with comprehensions, and process streams lazily with
generators.
"""

# 1. CONCEPT
# A comprehension builds a collection from an iterable in one expression:
#
#   [expr for x in xs if cond]        list
#   {k: v for k, v in pairs}          dict
#   {expr for x in xs}                set
#   (expr for x in xs)                generator expression (lazy, nothing computed yet)
#
# A generator function uses `yield`. Calling it returns an iterator; the body runs lazily,
# pausing at each `yield`. Generators are the tool for large or infinite streams: they hold
# one item in memory at a time.

import itertools
from collections.abc import Iterable, Iterator

# 2. EXAMPLES


def demo_comprehensions() -> None:
    nums = range(10)
    print([n * n for n in nums if n % 2 == 0])  # filter + transform
    print({word: len(word) for word in ["kiwi", "banana"]})
    print({len(word) for word in ["kiwi", "pear", "banana"]})
    print([(x, y) for x in range(2) for y in "ab"])  # nested loops: left to right
    matrix = [[1, 2], [3, 4], [5, 6]]
    print([cell for row in matrix for cell in row])  # flatten
    print(sum(n * n for n in range(1000)))  # generator expression, no list built


def read_in_batches(items: Iterable[int], size: int) -> Iterator[list[int]]:
    batch: list[int] = []
    for item in items:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch


def fibonacci() -> Iterator[int]:
    a, b = 0, 1
    while True:  # infinite, yet perfectly safe: values are produced on demand
        yield a
        a, b = b, a + b


def demo_generators() -> None:
    print(list(read_in_batches(range(7), 3)))
    print(list(itertools.islice(fibonacci(), 10)))

    gen = (n for n in range(3))
    print(list(gen), list(gen))  # second list is EMPTY: generators are one-shot

    names, ages = ["Ana", "Bob", "Cy"], [31, 25, 40]
    print(list(zip(names, ages)), dict(zip(names, ages)))
    print([f"{i}:{n}" for i, n in enumerate(names)])
    print(any(a > 35 for a in ages), all(a > 18 for a in ages))  # short-circuit


# 3. C# EQUIVALENT
#
#   Python                               C# / LINQ
#   -----------------------------------  ----------------------------------------
#   [f(x) for x in xs]                   xs.Select(f).ToList()
#   [x for x in xs if p(x)]              xs.Where(p).ToList()
#   {k: v for ...}                       xs.ToDictionary(...)
#   (f(x) for x in xs)                   xs.Select(f)   (deferred execution)
#   def gen(): yield x                   IEnumerable<T> with `yield return`
#   zip(a, b)                            a.Zip(b)
#   enumerate(xs)                        xs.Select((x, i) => (i, x))
#   any(...) / all(...)                  xs.Any(...) / xs.All(...)
#   itertools.islice(xs, n)              xs.Take(n)

# 4. COMMON PITFALLS
#
#   a) A generator can be consumed only once. Convert to a list if you need two passes.
#   b) Comprehensions with 3+ clauses get unreadable; use a normal loop or a helper function.
#   c) Do not use a comprehension for side effects ([print(x) for x in xs]); use a for loop.
#   d) A generator function's code does not run at call time, so errors surface on first next().

# 5. EXERCISE
# Open exercises/ex05_comprehensions.py, implement the functions, then run:
#     python runner.py test 05

if __name__ == "__main__":
    demo_comprehensions()
    print()
    demo_generators()
