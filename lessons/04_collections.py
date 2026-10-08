"""
Lesson 04: Collections

Goal: pick the right built-in collection and use slicing, sorting and `collections` helpers.
"""

# 1. CONCEPT
#
#   list   [1, 2, 3]       ordered, mutable, allows duplicates
#   tuple  (1, 2, 3)       ordered, IMMUTABLE, great for fixed records and dict keys
#   dict   {"a": 1}        key -> value, insertion-ordered (guaranteed since 3.7)
#   set    {1, 2, 3}       unordered, unique, fast membership; supports | & - ^
#
# Keys of dicts and members of sets must be *hashable* (immutable): str, int, tuple... not list.

from collections import Counter, defaultdict, deque

# 2. EXAMPLES


def demo_lists_and_slicing() -> None:
    nums = [10, 20, 30, 40, 50]
    print(
        nums[0], nums[-1], nums[1:3], nums[:2], nums[::2], nums[::-1]
    )  # slices are [start:stop:step]
    nums.append(60)
    nums.extend([70, 80])
    nums.insert(0, 0)
    print(nums, "| popped:", nums.pop(), "| length:", len(nums))

    ordered = sorted([3, 1, 2], reverse=True)  # sorted() returns a NEW list
    data = [3, 1, 2]
    data.sort()  # list.sort() sorts in place and returns None
    print(ordered, data)

    people = [("Ana", 31), ("Bob", 25), ("Cy", 31)]
    print(sorted(people, key=lambda p: (-p[1], p[0])))  # sort by age desc, then name


def demo_dicts() -> None:
    user = {"name": "Ana", "age": 31}
    user["email"] = "ana@example.com"
    print(user.get("phone"), user.get("phone", "n/a"), "age" in user)  # .get never raises
    for key, value in user.items():
        print(f"  {key} -> {value}")
    merged = user | {"age": 32}  # 3.9+: right side wins
    print(merged)
    print(user.setdefault("tags", []), user)  # insert default if the key is missing


def demo_sets_and_tuples() -> None:
    a, b = {1, 2, 3}, {3, 4}
    print(a | b, a & b, a - b, a ^ b, 2 in a)
    point = (3, 4)
    x, y = point  # unpacking
    first, *rest = [1, 2, 3, 4]
    print(x, y, first, rest)
    print(dict.fromkeys(["b", "a", "b"]))  # order-preserving de-duplication trick -> keys b, a


def demo_collections_module() -> None:
    print(Counter("mississippi").most_common(2))
    groups: defaultdict[str, list[str]] = defaultdict(list)  # missing key -> new empty list
    for word in ["apple", "avocado", "banana"]:
        groups[word[0]].append(word)
    print(dict(groups))
    queue = deque([1, 2, 3])  # O(1) at both ends
    queue.appendleft(0)
    queue.pop()
    print(queue)


# 3. C# EQUIVALENT
#
#   Python                      C#
#   --------------------------  ------------------------------------------
#   list                        List<T>
#   tuple                       ValueTuple / System.Tuple (immutable)
#   dict                        Dictionary<TKey, TValue>   (but insertion-ordered)
#   set                         HashSet<T>
#   d.get(k, default)           d.TryGetValue(k, out var v) ? v : default
#   defaultdict(list)           GetValueOrDefault + manual add
#   Counter                     GroupBy(...).ToDictionary(g => g.Key, g => g.Count())
#   deque                       LinkedList<T> / Queue<T>
#   nums[1:3], nums[::-1]       nums[1..3], Enumerable.Reverse(nums) (ranges, 8.0+)
#   sorted(xs, key=f)           xs.OrderBy(f)

# 4. COMMON PITFALLS
#
#   a) d["missing"] raises KeyError. Use d.get(...), `in`, or defaultdict.
#   b) [[0] * 3] * 3 creates 3 references to ONE inner list. Use [[0] * 3 for _ in range(3)].
#   c) {} is an empty DICT, not an empty set. Use set().
#   d) A tuple of one item needs a trailing comma: (1,) -- (1) is just the number 1.

# 5. EXERCISE
# Open exercises/ex04_collections.py, implement the functions, then run:
#     python runner.py test 04

if __name__ == "__main__":
    demo_lists_and_slicing()
    print()
    demo_dicts()
    print()
    demo_sets_and_tuples()
    print()
    demo_collections_module()
