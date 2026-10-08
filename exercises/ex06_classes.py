"""Exercise 06: classes and dataclasses.

Read lessons/06_classes_and_dataclasses.py first. The classes below are placeholders:
replace each stub with a real implementation (prefer @dataclass where it fits).
Run the tests with:  python runner.py test 06
"""


class Vehicle:
    """A fleet vehicle. Implement it as a ``@dataclass``.

    Fields (in this order): ``plate: str``, ``model: str``, ``odometer_km: float = 0.0``.

    - ``drive(km)``: add ``km`` to the odometer. ``km <= 0`` raises ``ValueError``.
    - ``is_new`` (a read-only ``@property``): True while the odometer is below 100 km.
    - Instances with equal fields compare equal; the default ``repr`` shows the plate.

    Example:
        v = Vehicle("ABC1D23", "Van"); v.drive(250.5); v.odometer_km -> 250.5
    """

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class Truck(Vehicle):
    """A ``Vehicle`` that also has ``capacity_kg: float = 1000.0``.

    - ``can_carry(weight_kg)``: True if ``weight_kg <= capacity_kg``.
    - ``Truck("T1", "Volvo", capacity_kg=5000)`` must work (inherit from Vehicle and add a field).
    """


class Position:
    """A geographic point. Implement it as an immutable (``frozen``) ``@dataclass``.

    Fields: ``lat: float``, ``lon: float``.

    - assigning to a field after creation must fail (frozen)
    - instances must be hashable (usable as dict keys / in sets)
    - ``is_valid`` (property): True if -90 <= lat <= 90 and -180 <= lon <= 180
    """

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class Fleet:
    """A collection of vehicles keyed by plate, implemented with dunder methods.

    - ``Fleet()`` starts empty; ``add(vehicle)`` stores it and raises ``ValueError`` if a
      vehicle with the same plate already exists
    - ``len(fleet)``: number of vehicles
    - ``for v in fleet``: iterates vehicles in insertion order
    - ``"ABC1D23" in fleet``: membership by plate
    - ``fleet["ABC1D23"]``: lookup by plate, ``KeyError`` if missing
    - ``total_km`` (property): sum of every vehicle's odometer
    """

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


def sort_vehicles_by_odometer(vehicles: list[Vehicle], descending: bool = False) -> list[Vehicle]:
    """Return a NEW list sorted by ``odometer_km`` (ascending unless ``descending``).

    The input list must not be modified.
    """
    raise NotImplementedError
