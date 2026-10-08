"""
Lesson 06: Classes and dataclasses

Goal: write Pythonic classes, reach for @dataclass first, and use dunder methods to make
your objects behave like built-ins.
"""

# 1. CONCEPT
# A class is created with `class`. `__init__` is the initializer (not exactly a constructor),
# and `self` is an explicit first parameter. There are no access modifiers: a leading
# underscore (`_x`) is a *convention* meaning "internal".
#
# Dunder ("double underscore") methods plug your class into the language:
#   __repr__ (debug text), __str__ (display text), __eq__, __lt__, __len__, __iter__,
#   __contains__, __getitem__, __enter__/__exit__ ...
#
# @dataclass generates __init__, __repr__ and __eq__ from annotated fields. Options:
#   frozen=True (immutable + hashable), order=True (comparison), slots=True, kw_only=True.

from dataclasses import dataclass, field

# 2. EXAMPLES


class Temperature:
    """The long way: a plain class with a property."""

    def __init__(self, celsius: float) -> None:
        self._celsius = celsius  # leading underscore: "please don't touch directly"

    @property
    def celsius(self) -> float:  # read like an attribute: t.celsius
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:  # validated assignment: t.celsius = 5
        if value < -273.15:
            raise ValueError("below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:  # computed, read-only property
        return self._celsius * 9 / 5 + 32

    def __repr__(self) -> str:  # unambiguous, for developers
        return f"Temperature(celsius={self._celsius})"


@dataclass(order=True)
class Player:
    """The short way: @dataclass writes __init__, __repr__, __eq__ and ordering for you."""

    score: int  # order=True compares fields in declaration order
    name: str = field(compare=False)  # ... except this one
    tags: list[str] = field(default_factory=list, compare=False)  # mutable default -> factory!


@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def distance_to(self, other: "Point") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


class Animal:
    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> str:
        return "..."

    def __str__(self) -> str:
        return f"{type(self).__name__} {self.name} says {self.speak()}"


class Dog(Animal):  # inheritance: class Child(Parent)
    def __init__(self, name: str, tricks: int = 0) -> None:
        super().__init__(name)  # call the parent initializer explicitly
        self.tricks = tricks

    def speak(self) -> str:  # override; no `virtual`/`override` keywords needed
        return "woof"


class Playlist:
    """Dunder methods make a class feel built in."""

    def __init__(self, *songs: str) -> None:
        self._songs = list(songs)

    def __len__(self) -> int:
        return len(self._songs)

    def __iter__(self):  # makes `for song in playlist` work
        return iter(self._songs)

    def __contains__(self, song: str) -> bool:  # makes `"x" in playlist` work
        return song in self._songs

    def __getitem__(self, index: int) -> str:  # makes playlist[0] work
        return self._songs[index]


def demo() -> None:
    t = Temperature(100)
    t.celsius = 37
    print(t, t.fahrenheit)

    a, b = Player(10, "Ana"), Player(7, "Bob")
    print(a, a == Player(10, "Someone else"), a > b, sorted([a, b]))

    p = Point(0, 0)
    print(p, p.distance_to(Point(3, 4)), {p: "usable as dict key"})
    try:
        p.x = 5  # type: ignore[misc]
    except AttributeError as err:  # dataclasses.FrozenInstanceError
        print("frozen:", type(err).__name__)

    print(Dog("Rex", tricks=2), "|", isinstance(Dog("Rex"), Animal))

    playlist = Playlist("a", "b", "c")
    print(len(playlist), "b" in playlist, playlist[0], list(playlist))


# 3. C# EQUIVALENT
#
#   Python                          C#
#   ------------------------------  ----------------------------------------------
#   class Foo: def __init__(self)   class Foo { public Foo() {...} }
#   self.x = x                      this.X = x   (every instance attribute is "public")
#   _x convention                   private field (not enforced in Python)
#   @property                       property { get; set; }
#   @dataclass                      record / record class
#   @dataclass(frozen=True)         record with init-only properties (immutable)
#   field(default_factory=list)     = new List<T>() initializer
#   super().__init__(...)           : base(...)
#   __repr__ / __str__              ToString()
#   __eq__ / __hash__               Equals / GetHashCode
#   __len__, __iter__, __getitem__  Count, IEnumerable<T>, indexer this[int i]
#   duck typing / Protocol          interfaces (see lesson 11)

# 4. COMMON PITFALLS
#
#   a) Don't write getters/setters by default. Use a plain attribute; promote it to a
#      @property later if you need validation (callers don't change).
#   b) A mutable class-level attribute (`items = []`) is shared by all instances.
#   c) Dataclass mutable defaults need field(default_factory=list); `= []` raises ValueError.
#   d) Forgetting `self` in a method definition gives a confusing TypeError about argument count.

# 5. EXERCISE
# Open exercises/ex06_classes.py, implement the classes, then run:
#     python runner.py test 06

if __name__ == "__main__":
    demo()
