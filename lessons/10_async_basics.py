"""
Lesson 10: Async basics

Goal: write concurrent I/O code with asyncio: coroutines, tasks, gather and timeouts.
"""

# 1. CONCEPT
# `async def` defines a *coroutine function*. Calling it does NOT run it: it returns a
# coroutine object. Something has to drive it:
#   - `await coro`            run it and wait for the result (only inside another async def)
#   - `asyncio.run(coro)`     entry point: starts an event loop and runs until done
#   - `asyncio.create_task`   schedule it to run concurrently, get a Task back
#   - `asyncio.gather(*coros)` run many concurrently, collect results IN ORDER
#
# asyncio is single-threaded cooperative multitasking: tasks switch only at `await` points.
# It shines for I/O-bound work (network, files via libraries); it does NOT speed up CPU-bound
# work (use multiprocessing for that) and a blocking call (time.sleep, requests.get) freezes
# the whole loop.

import asyncio
import time

# 2. EXAMPLES


async def fetch(name: str, delay: float) -> str:
    await asyncio.sleep(delay)  # non-blocking sleep: yields control to other tasks
    return f"{name} (after {delay}s)"


async def demo_sequential_vs_concurrent() -> None:
    start = time.perf_counter()
    first = await fetch("a", 0.2)
    second = await fetch("b", 0.2)  # starts only after the first finished
    print(f"sequential: {time.perf_counter() - start:.1f}s ->", first, "|", second)

    start = time.perf_counter()
    results = await asyncio.gather(fetch("a", 0.2), fetch("b", 0.2), fetch("c", 0.2))
    print(f"gather:     {time.perf_counter() - start:.1f}s ->", results)


async def demo_tasks_and_timeouts() -> None:
    task = asyncio.create_task(fetch("background", 0.1))  # starts running immediately
    print("task created, doing other work...")
    print("task result:", await task)

    try:
        await asyncio.wait_for(fetch("slow", 1.0), timeout=0.1)
    except TimeoutError:  # asyncio.TimeoutError is the same class since 3.11
        print("timed out")


async def demo_errors() -> None:
    async def boom() -> None:
        raise RuntimeError("boom")

    results = await asyncio.gather(fetch("ok", 0.01), boom(), return_exceptions=True)
    print("gather(return_exceptions=True):", results)  # errors are returned, not raised


async def main() -> None:
    await demo_sequential_vs_concurrent()
    await demo_tasks_and_timeouts()
    await demo_errors()


# 3. C# EQUIVALENT
#
#   Python                            C#
#   --------------------------------  ----------------------------------------
#   async def f() -> int              async Task<int> F()
#   await x                           await x
#   asyncio.run(main())               await Main() (or Task.Run(...).GetAwaiter().GetResult())
#   asyncio.create_task(c)            Task.Run(...) / starting a Task without awaiting
#   asyncio.gather(a, b)              await Task.WhenAll(a, b)
#   asyncio.wait_for(c, timeout=1)    CancellationTokenSource(timeout) / Task.WaitAsync(timeout)
#   asyncio.sleep(1)                  await Task.Delay(1000)
#   asyncio.Queue                     Channel<T>
#   asyncio.Lock / Semaphore          SemaphoreSlim
#   KEY DIFFERENCE                    a Python coroutine is lazy: it does nothing until awaited
#                                     or scheduled; a C# Task is already running when returned

# 4. COMMON PITFALLS
#
#   a) Forgetting `await`: you get a coroutine object and a "never awaited" warning.
#   b) `time.sleep()` or blocking I/O inside async code blocks every other task. Use
#      `await asyncio.sleep()` / async libraries, or `await asyncio.to_thread(blocking_fn)`.
#   c) `await a(); await b()` is sequential. Use gather/create_task for concurrency.
#   d) Don't call `asyncio.run()` from inside a running loop (e.g. in a notebook or another
#      coroutine); just `await`.

# 5. EXERCISE
# Open exercises/ex10_async.py, implement the functions, then run:
#     python runner.py test 10

if __name__ == "__main__":
    asyncio.run(main())
