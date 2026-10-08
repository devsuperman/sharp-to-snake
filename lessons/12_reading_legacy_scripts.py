"""
Lesson 12: Reading legacy scripts

Goal: take a Python script you did not write, work out what it does, and find the things a
migration to C# must not lose (inputs, outputs, hidden state, silent error handling).
"""

# 1. CONCEPT
# Most automation scripts grow organically: one file, code at module level, globals, little
# error handling, no tests. Before rewriting anything, READ it with a checklist:
#
#   Entry point   what runs first? (`if __name__ == "__main__":`, or just top-level code?)
#   Inputs        sys.argv, os.environ, files, stdin, network calls, the clock
#   Outputs       files written, API calls, prints, the exit code
#   Hidden state  module-level variables mutated through `global`
#   Error policy  bare `except:`, `except ...: pass`, retries, sleeps
#   Implicit rules  magic numbers, filters, unit and timezone assumptions
#
# The implicit rules are the dangerous part: they are business rules that nobody documented
# and that the old script enforces by accident. A migration that misses one changes behaviour.
#
# Two tools help you read code you do not trust:
#   - run it with test data and watch (a "characterization test" records what it does today)
#   - the `ast` module, which parses source into a tree WITHOUT running it

import ast
import textwrap

# 2. EXAMPLES

LEGACY = textwrap.dedent(
    """
    import os
    import sys
    import requests

    URL = os.environ.get("EXPORT_URL", "http://localhost/api")
    count = 0

    def push(rows):
        global count
        for row in rows:
            try:
                requests.post(URL, json=row)
                count += 1
            except:
                pass

    push(open(sys.argv[1]).read().split())
    print("done", count)
    """
)


def demo_ast_inventory() -> None:
    tree = ast.parse(LEGACY)  # parsing never executes the code
    for node in ast.walk(tree):  # visits every node of the tree, parents before children
        if isinstance(node, ast.FunctionDef):
            print(
                f"function {node.name}({', '.join(a.arg for a in node.args.args)}) "
                f"at line {node.lineno}"
            )
    top_level_calls = [
        n for n in tree.body if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
    ]
    print("calls that run at import time:", len(top_level_calls))  # push(...) and print(...)


def demo_why_globals_hurt() -> None:
    counter = 0

    def bump_wrong() -> None:
        counter = 1  # creates a NEW local variable; the outer one is untouched
        _ = counter

    def bump_right() -> None:
        nonlocal counter  # `global` for module level, `nonlocal` for an enclosing function
        counter += 1

    bump_wrong()
    print("after bump_wrong:", counter)
    bump_right()
    print("after bump_right:", counter)


def demo_refactor_for_testing() -> None:
    # Before: reads os.environ at import, mutates a global, runs on import. Hard to test.
    # After: an explicit config object in, an explicit result out, no side effects on import.
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class Config:
        url: str

    def push(rows: list[str], config: Config, send) -> int:
        sent = 0
        for row in rows:
            send(config.url, row)
            sent += 1
        return sent

    calls: list[tuple[str, str]] = []
    print(push(["a", "b"], Config("http://x"), lambda u, r: calls.append((u, r))), calls)


def demo() -> None:
    demo_ast_inventory()
    demo_why_globals_hurt()
    demo_refactor_for_testing()


# 3. C# EQUIVALENT
#
#   Python                                    C#
#   ----------------------------------------  ---------------------------------------------
#   top-level script code                     top-level statements (Program.cs)
#   if __name__ == "__main__": main()         static Main / top-level entry point
#   os.environ.get("X", "d")                  configuration["X"] ?? "d" (IConfiguration)
#   sys.argv                                  string[] args
#   global counter                            a static mutable field (also a smell in C#)
#   injecting `send` as a parameter           constructor/DI injection of an interface
#   bare `except:`                            catch { } (swallows even Ctrl-C and SystemExit)
#   ast.parse(source)                         Roslyn: CSharpSyntaxTree.ParseText(source)
#   characterization test                     "golden master" / approval test (ApprovalTests)

# 4. COMMON PITFALLS
#
#   a) `except:` also catches KeyboardInterrupt and SystemExit; `except Exception:` does not,
#      but `except Exception: pass` still hides every bug. Look for both when reading.
#   b) Module-level code runs on IMPORT. Importing a legacy script in a test may start the job.
#   c) Assigning to a name inside a function creates a local; mutating needs `global`/`nonlocal`.
#   d) Naive datetimes (no timezone) hide assumptions such as "the server is in UTC-3".
#   e) Truthiness: `if not value` is also true for 0, "" and [] -- is that really intended?
#   f) Do not trust comments or names; trust behaviour. Run it, record it, then rewrite it.

# 5. EXERCISE
# Open exercises/ex12_legacy_scripts.py, implement the functions, then run:
#     python runner.py test 12

if __name__ == "__main__":
    demo()
