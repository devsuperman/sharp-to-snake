"""Exercise 09: build a small package.

Read lessons/09_modules_and_packages.py first. Layout of this package:

    ex09_textkit/
        __init__.py   <- you: re-export the public API with RELATIVE imports + define __all__
        slug.py       <- you: implement slugify()
        counts.py     <- you: implement word_count()
        __main__.py   <- you: make `python -m exercises.ex09_textkit "Some Text"` work

Requirements:
- ``from exercises.ex09_textkit import slugify, word_count`` must work.
- ``__all__`` must be exactly ``["slugify", "word_count"]`` (any order).
- Importing the package must not print anything (no side effects at import time).
- Running ``python -m exercises.ex09_textkit "Hello, World!  Again"`` prints the slug on the
  first line and the word count on the second:
      hello-world-again
      3

Run the tests with:  python runner.py test 09
"""
