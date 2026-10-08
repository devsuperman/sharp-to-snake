import dataclasses

import pytest

from exercises.ex06_classes import Fleet, Position, Truck, Vehicle, sort_vehicles_by_odometer


def test_vehicle_is_a_dataclass_with_defaults():
    assert dataclasses.is_dataclass(Vehicle)
    vehicle = Vehicle("ABC1D23", "Van")
    assert vehicle.odometer_km == 0.0


def test_vehicle_equality_and_repr():
    assert Vehicle("A", "Van", 10) == Vehicle("A", "Van", 10)
    assert Vehicle("A", "Van") != Vehicle("B", "Van")
    assert "ABC1D23" in repr(Vehicle("ABC1D23", "Van"))


def test_vehicle_drive_accumulates():
    vehicle = Vehicle("A", "Van")
    vehicle.drive(100)
    vehicle.drive(150.5)
    assert vehicle.odometer_km == pytest.approx(250.5)


@pytest.mark.parametrize("km", [0, -5])
def test_vehicle_drive_rejects_non_positive(km):
    with pytest.raises(ValueError):
        Vehicle("A", "Van").drive(km)


def test_vehicle_is_new_property():
    assert Vehicle("A", "Van", 99.9).is_new is True
    assert Vehicle("A", "Van", 100).is_new is False
    with pytest.raises(AttributeError):
        Vehicle("A", "Van").is_new = False  # read-only property


def test_truck_inherits_and_carries():
    truck = Truck("T1", "Volvo", capacity_kg=5000)
    assert isinstance(truck, Vehicle)
    assert truck.can_carry(5000) is True
    assert truck.can_carry(5000.1) is False
    assert Truck("T2", "Scania").capacity_kg == 1000.0
    truck.drive(10)
    assert truck.odometer_km == 10


def test_position_is_frozen_and_hashable():
    position = Position(10.0, 20.0)
    with pytest.raises(dataclasses.FrozenInstanceError):
        position.lat = 5.0  # type: ignore[misc]
    assert {position: "x"}[Position(10.0, 20.0)] == "x"


@pytest.mark.parametrize(
    ("lat", "lon", "valid"),
    [(0, 0, True), (90, 180, True), (-90, -180, True), (90.1, 0, False), (0, -180.5, False)],
)
def test_position_is_valid(lat, lon, valid):
    assert Position(lat, lon).is_valid is valid


def test_fleet_collection_protocol():
    fleet = Fleet()
    assert len(fleet) == 0
    van, truck = Vehicle("A1", "Van", 100), Truck("T1", "Volvo", 50)
    fleet.add(van)
    fleet.add(truck)
    assert len(fleet) == 2
    assert list(fleet) == [van, truck]
    assert "A1" in fleet
    assert "ZZZ" not in fleet
    assert fleet["T1"] is truck
    assert fleet.total_km == 150


def test_fleet_rejects_duplicates_and_unknown_plates():
    fleet = Fleet()
    fleet.add(Vehicle("A1", "Van"))
    with pytest.raises(ValueError):
        fleet.add(Vehicle("A1", "Other"))
    with pytest.raises(KeyError):
        fleet["nope"]


def test_sort_vehicles_by_odometer():
    a, b, c = Vehicle("A", "x", 30), Vehicle("B", "x", 10), Vehicle("C", "x", 20)
    original = [a, b, c]
    assert sort_vehicles_by_odometer(original) == [b, c, a]
    assert sort_vehicles_by_odometer(original, descending=True) == [a, c, b]
    assert original == [a, b, c]
