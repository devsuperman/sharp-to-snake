"""Exercise 02: control flow.

Read lessons/02_control_flow.py first, then implement every function below.
Run the tests with:  python runner.py test 02
"""


def fizzbuzz(n: int) -> list[str]:
    """Return the FizzBuzz sequence from 1 to ``n`` inclusive, as strings.

    Multiples of 3 -> "Fizz", of 5 -> "Buzz", of both -> "FizzBuzz"; otherwise the number.
    ``n <= 0`` gives an empty list.

    Example:
        fizzbuzz(5)  -> ["1", "2", "Fizz", "4", "Buzz"]
    """
    raise NotImplementedError


def classify(value: object) -> str:
    """Classify ``value`` with a ``match`` statement.

    None            -> "nothing"
    bool            -> "boolean"   (check before int!)
    0               -> "zero"
    other int       -> "integer"
    str             -> "text"
    list or tuple   -> "sequence"
    anything else   -> "unknown"

    Examples:
        classify(None) -> "nothing";  classify(True) -> "boolean";  classify(7) -> "integer"
    """
    raise NotImplementedError


def first_primes(count: int) -> list[int]:
    """Return the first ``count`` prime numbers using loops (``while`` is a good fit).

    Examples:
        first_primes(5) -> [2, 3, 5, 7, 11]
        first_primes(0) -> []
    """
    raise NotImplementedError


def index_of_first_negative(values: list[int]) -> int | None:
    """Return the index of the first negative number, or None if there is none.

    Use a loop with ``break`` or an early ``return``.

    Examples:
        index_of_first_negative([3, 0, -2, -5]) -> 2
        index_of_first_negative([1, 2])         -> None
    """
    raise NotImplementedError
