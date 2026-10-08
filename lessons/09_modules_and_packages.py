"""
Lesson 09: Modules and packages

Goal: understand how imports resolve, how to structure a package, and what
`if __name__ == "__main__"` really does.
"""

# 1. CONCEPT
# - A *module* is any .py file. `import mymodule` runs it once and caches it in sys.modules.
# - A *package* is a directory with an `__init__.py` (that file runs when the package is
#   imported and defines what the package exposes).
# - Absolute imports: `from mypkg.text import slugify`.
# - Relative imports (inside a package only): `from .text import slugify`, `from ..other import x`.
# - `python -m mypkg` runs `mypkg/__main__.py` (this is how `python -m venv` and `python -m pytest` work).
# - Every module has `__name__`: it is "__main__" when run as a script, otherwise its dotted path.
#   The `if __name__ == "__main__":` guard keeps demo/CLI code from running on import.
# - `__all__` lists the names exported by `from module import *` and documents the public API.
# - Third-party packages come from PyPI via `pip install <name>`, always inside a venv.

import importlib
import sys
import tempfile
import textwrap
from pathlib import Path

# 2. EXAMPLES


def demo_module_basics() -> None:
    import math  # a stdlib module

    print("module name:", math.__name__, "| this file's __name__:", __name__)
    from math import sqrt as square_root  # import a name, optionally renamed

    print(square_root(16), "| already cached:", "math" in sys.modules)
    print("search path starts with:", sys.path[0])


def build_demo_package(root: Path) -> None:
    """Create a tiny package on disk so we can import it for real."""
    package = root / "shapes"
    package.mkdir()
    (package / "__init__.py").write_text(
        textwrap.dedent(
            '''
            """Public API of the shapes package."""
            from .circle import area as circle_area
            from .square import area as square_area

            __all__ = ["circle_area", "square_area"]
            print("  (shapes/__init__.py ran)")
            '''
        ),
        encoding="utf-8",
    )
    (package / "circle.py").write_text(
        "import math\n\ndef area(r):\n    return math.pi * r**2\n", encoding="utf-8"
    )
    (package / "square.py").write_text(
        "def area(side):\n    return side * side\n", encoding="utf-8"
    )
    (package / "__main__.py").write_text(
        "from . import circle_area\nprint('python -m shapes ->', round(circle_area(1), 2))\n",
        encoding="utf-8",
    )


def demo_package() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        build_demo_package(Path(tmp))
        sys.path.insert(0, tmp)  # make the temp directory importable
        try:
            shapes = importlib.import_module("shapes")  # runs __init__.py once
            importlib.import_module("shapes")  # second import: cached, no output
            print("circle:", round(shapes.circle_area(2), 2), "| square:", shapes.square_area(3))
            print("exports:", shapes.__all__, "| submodule:", shapes.circle.__name__)
        finally:
            sys.path.remove(tmp)
            for name in [m for m in sys.modules if m == "shapes" or m.startswith("shapes.")]:
                del sys.modules[name]


def demo() -> None:
    demo_module_basics()
    print()
    demo_package()


# 3. C# EQUIVALENT
#
#   Python                         C#
#   -----------------------------  ------------------------------------------------
#   module (.py file)              source file / static class
#   package (dir + __init__.py)    namespace (and, loosely, an assembly)
#   import x / from x import y     using X; / using static X;
#   __init__.py                    no equivalent (assembly metadata + global usings, loosely)
#   __all__                        `public` vs `internal` visibility
#   if __name__ == "__main__":     static Main() (Program entry point)
#   pip + venv + requirements      NuGet + PackageReference + project-local packages
#   pyproject.toml                 .csproj / Directory.Build.props
#   sys.path                       probing paths / assembly resolution

# 4. COMMON PITFALLS
#
#   a) Circular imports (a imports b imports a) cause ImportError. Move shared code to a third
#      module, or import inside the function.
#   b) Naming a file like a stdlib module (`random.py`, `json.py`) shadows it. Never do that.
#   c) Relative imports fail when the file is run directly (`python pkg/mod.py`); run it with
#      `python -m pkg.mod` instead.
#   d) `from x import *` pollutes the namespace. Import what you need, explicitly.
#   e) Code at module top level runs on import: keep it free of side effects.

# 5. EXERCISE
# Open exercises/ex09_textkit/ (a package of stubs), implement it, then run:
#     python runner.py test 09

if __name__ == "__main__":
    demo()
