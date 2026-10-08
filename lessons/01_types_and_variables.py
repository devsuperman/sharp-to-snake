"""
Lesson 01: Types and variables

Goal: understand Python's dynamic typing, its core built-in types, and what "mutable" means.
"""

# 1. CONCEPT
# Python is dynamically typed: a *name* is just a label that points at an object, and the
# *object* carries the type. There is no declaration; assignment creates the name.
#
#   int, float, str, bool, None   -> the core scalar types
#   int has arbitrary precision   -> no overflow, ever
#   str is immutable              -> every "modification" creates a new string
#   list is mutable               -> shared references see in-place changes
#   None is the single "no value" object (compare with `is None`, not `== None`)

# 2. EXAMPLES


def demo_dynamic_typing() -> None:
    x = 42
    print("x =", x, type(x))
    x = "now a string"  # legal: the name was just re-pointed at a different object
    print("x =", x, type(x))
    print("2 ** 100 =", 2**100)  # no overflow
    print("7 / 2 =", 7 / 2, "| 7 // 2 =", 7 // 2, "| -7 // 2 =", -7 // 2, "| 7 % 3 =", 7 % 3)


def demo_f_strings() -> None:
    name, price = "Ana", 1234.5678
    print(f"Hello, {name}!")
    print(f"Price: {price:,.2f}")  # format spec after ':'  -> 1,234.57
    print(f"{name=}")  # debugging helper -> name='Ana'
    print(f"{'left':<8}|{'right':>8}|{42:^8}|{42:08.3f}")


def demo_none_and_truthiness() -> None:
    value = None
    print("is None:", value is None)
    # Falsy values: None, False, 0, 0.0, "", [], {}, set(), ()  -- everything else is truthy
    for candidate in (None, 0, "", [], "0", [0]):
        print(f"bool({candidate!r}) ->", bool(candidate))


def demo_mutability() -> None:
    a = [1, 2, 3]
    b = a  # b is NOT a copy: both names point at the same list
    b.append(4)
    print("a:", a, "| same object:", a is b)

    c = a.copy()  # shallow copy
    c.append(5)
    print("a:", a, "| c:", c, "| same object:", a is c)

    s = "abc"
    t = s.upper()  # strings are immutable: upper() returns a NEW string
    print("s:", s, "| t:", t)


# 3. C# EQUIVALENT
#
#   Python                         C#
#   -----------------------------  ------------------------------------------------
#   x = 42                         var x = 42;   (but Python can re-point x at a str)
#   f"Hi {name}"                   $"Hi {name}"
#   None / `is None`               null / `is null`
#   int (unbounded)                BigInteger (int/long overflow in C#)
#   //  and  %                     Math.Floor(a / b), and a modulo that follows the divisor's sign
#   list                           List<object>   (reference semantics, like any class)
#   str                            string (also immutable)
#   type(x), isinstance(x, int)    x.GetType(), x is int
#   "truthy" / "falsy"             no equivalent: C# `if` demands a bool

# 4. COMMON PITFALLS
#
#   a) bool is a subclass of int:  isinstance(True, int) is True. Check bool *first*.
#   b) `b = a` never copies. Use a.copy(), list(a), or a[:] for a shallow copy.
#   c) `==` compares values, `is` compares identity. Use `is` only for None/True/False.
#   d) int("3.5") raises ValueError; int(3.9) truncates to 3. Parse defensively.

# 5. EXERCISE
# Open exercises/ex01_types.py, implement the functions, then run:
#     python runner.py test 01

if __name__ == "__main__":
    demo_dynamic_typing()
    print()
    demo_f_strings()
    print()
    demo_none_and_truthiness()
    print()
    demo_mutability()
