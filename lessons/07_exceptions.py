"""
Lesson 07: Exceptions

Goal: handle and raise errors idiomatically, design a small exception hierarchy, and
understand EAFP vs LBYL.
"""

# 1. CONCEPT
#
#   try:        code that may fail
#   except X:   handle a specific exception type (list the most specific first)
#   else:       runs only if the try block raised nothing
#   finally:    always runs (cleanup)
#   raise X     raise; a bare `raise` inside `except` re-raises the current exception
#   raise X from Y   chain: Y is stored in X.__cause__ ("caused by")
#
# Everything you raise must derive from BaseException; in practice from Exception.
# Python culture favours EAFP ("Easier to Ask Forgiveness than Permission"): just try the
# operation and handle the failure, instead of LBYL ("Look Before You Leap") pre-checks.

# 2. EXAMPLES


class AppError(Exception):
    """Base class for this application's errors."""


class ConfigError(AppError):
    def __init__(self, key: str, message: str = "invalid configuration") -> None:
        super().__init__(f"{key}: {message}")  # becomes str(exc)
        self.key = key  # extra structured data


def parse_port(raw: str) -> int:
    try:
        port = int(raw)
    except ValueError as err:
        raise ConfigError("port", f"not a number: {raw!r}") from err  # keep the original cause
    if not 0 < port < 65536:
        raise ConfigError("port", "out of range")
    return port


def demo_try_except_else_finally() -> None:
    for raw in ("8080", "abc", "70000"):
        try:
            port = parse_port(raw)
        except ConfigError as err:
            print(f"  {raw!r}: ConfigError({err}) cause={err.__cause__!r}")
        else:
            print(f"  {raw!r}: OK -> {port}")
        finally:
            print("  (finally always runs)")


def demo_eafp_vs_lbyl() -> None:
    data = {"a": 1}
    # LBYL: check first (two lookups, and racy in real life for files, sockets, ...)
    value = data["b"] if "b" in data else None
    # EAFP: try it, handle the rare failure
    try:
        value = data["b"]
    except KeyError:
        value = None
    print("EAFP/LBYL value:", value)


def demo_multiple_except() -> None:
    for payload in ({"n": "5"}, {}, {"n": "x"}, None):
        try:
            print("  result:", 10 / int(payload["n"]))  # type: ignore[index]
        except (KeyError, TypeError) as err:  # several types in one clause
            print("  bad payload:", type(err).__name__)
        except ValueError:
            print("  not an integer")


def demo_context_manager() -> None:
    from contextlib import suppress

    with suppress(FileNotFoundError):  # ignore one specific error, explicitly
        open("/definitely/not/here.txt").close()
    print("  suppressed FileNotFoundError")


def demo() -> None:
    demo_try_except_else_finally()
    demo_eafp_vs_lbyl()
    demo_multiple_except()
    demo_context_manager()


# 3. C# EQUIVALENT
#
#   Python                          C#
#   ------------------------------  ------------------------------------
#   try / except / else / finally   try / catch / (no else) / finally
#   except (A, B) as err:           catch (Exception err) when (err is A or B)
#   raise X from Y                  throw new X("...", innerException: y)
#   bare `raise`                    throw;
#   class MyError(Exception)        class MyException : Exception
#   with open(...) as f:            using var f = File.OpenRead(...)
#   KeyError / IndexError           KeyNotFoundException / IndexOutOfRangeException
#   ValueError / TypeError          FormatException|ArgumentException / InvalidCastException
#   exceptions are cheap & common   exceptions are expensive: Python uses them for flow control

# 4. COMMON PITFALLS
#
#   a) A bare `except:` (or `except Exception: pass`) hides bugs. Catch specific types.
#   b) `raise X` inside `except` without `from` still chains implicitly; `from None` hides it.
#   c) Don't catch BaseException: it includes KeyboardInterrupt and SystemExit.
#   d) `else` is for code that should run only on success but must not be protected by
#      the `except`. It keeps the try block small.

# 5. EXERCISE
# Open exercises/ex07_exceptions.py, implement the functions, then run:
#     python runner.py test 07

if __name__ == "__main__":
    demo()
