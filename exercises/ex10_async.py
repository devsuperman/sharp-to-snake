"""Exercise 10: async basics.

Read lessons/10_async_basics.py first, then implement every function below.
Run the tests with:  python runner.py test 10
"""


async def fetch_resource(name: str, delay: float = 0.05) -> str:
    """Simulate a network call: wait ``delay`` seconds (non-blocking), then return the name
    in the form ``"resource:<name>"``.

    Example:
        await fetch_resource("users") -> "resource:users"
    """
    raise NotImplementedError


async def fetch_all(names: list[str], delay: float = 0.05) -> list[str]:
    """Fetch every name CONCURRENTLY and return the results in the same order as ``names``.

    Ten names with a 0.1 s delay must take roughly 0.1 s in total, not 1 s.

    Example:
        await fetch_all(["a", "b"]) -> ["resource:a", "resource:b"]
    """
    raise NotImplementedError


async def fetch_with_timeout(name: str, delay: float, timeout: float) -> str | None:
    """Fetch one resource but give up after ``timeout`` seconds.

    Return the resource string on success, or None if it timed out.

    Examples:
        await fetch_with_timeout("a", delay=0.01, timeout=1)  -> "resource:a"
        await fetch_with_timeout("a", delay=1,    timeout=0.05) -> None
    """
    raise NotImplementedError


async def fetch_all_tolerant(
    names: list[str], failing: set[str], delay: float = 0.01
) -> list[str | None]:
    """Fetch concurrently, but names listed in ``failing`` raise an error inside their task.

    Return results in input order, with None in place of every failed fetch. One failure must
    not cancel the others.

    Hint: ``asyncio.gather(..., return_exceptions=True)``.

    Example:
        await fetch_all_tolerant(["a", "b", "c"], failing={"b"})
        -> ["resource:a", None, "resource:c"]
    """
    raise NotImplementedError
