import asyncio
import time

import pytest

from exercises.ex10_async import (
    fetch_all,
    fetch_all_tolerant,
    fetch_resource,
    fetch_with_timeout,
)


def test_fetch_resource():
    assert asyncio.run(fetch_resource("users", delay=0)) == "resource:users"


def test_fetch_resource_really_waits():
    start = time.perf_counter()
    asyncio.run(fetch_resource("x", delay=0.1))
    assert time.perf_counter() - start >= 0.09


def test_fetch_all_preserves_order():
    names = ["a", "b", "c"]
    assert asyncio.run(fetch_all(names, delay=0.01)) == ["resource:a", "resource:b", "resource:c"]


def test_fetch_all_empty():
    assert asyncio.run(fetch_all([])) == []


def test_fetch_all_runs_concurrently():
    start = time.perf_counter()
    result = asyncio.run(fetch_all([str(i) for i in range(10)], delay=0.2))
    elapsed = time.perf_counter() - start
    assert len(result) == 10
    assert elapsed < 1.0, f"took {elapsed:.2f}s: looks sequential (expected ~0.2s)"


@pytest.mark.parametrize(
    ("delay", "timeout", "expected"),
    [(0.01, 1.0, "resource:a"), (1.0, 0.05, None)],
)
def test_fetch_with_timeout(delay, timeout, expected):
    start = time.perf_counter()
    assert asyncio.run(fetch_with_timeout("a", delay=delay, timeout=timeout)) == expected
    assert time.perf_counter() - start < 0.9  # a timed-out fetch must not wait for the full delay


def test_fetch_all_tolerant_replaces_failures_with_none():
    result = asyncio.run(fetch_all_tolerant(["a", "b", "c"], failing={"b"}))
    assert result == ["resource:a", None, "resource:c"]


def test_fetch_all_tolerant_without_failures():
    assert asyncio.run(fetch_all_tolerant(["a"], failing=set())) == ["resource:a"]
