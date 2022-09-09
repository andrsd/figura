import pytest
from figura.geometry import (
    Point,
    Direction,
    Axis2
)
from figura.primitives import (
    Box,
    Cylinder,
    Sphere,
    Cone
)


def test_name():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 2, 3)
    box = Box(pt1, pt2)
    box.name("box")
    assert box.name() == "box"


def test_wrong_name_type():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 2, 3)
    box = Box(pt1, pt2)
    with pytest.raises(TypeError):
        box.name(123)


def test_box():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 2, 3)
    Box(pt1, pt2)


def test_cylinder():
    pt = Point(0, 0, 0)
    dir = Direction(0, 0, 1)
    axis = Axis2(pt, dir)
    Cylinder(axis, 0.5, 2)


def test_sphere():
    pt = Point(0, 0, 0)
    Sphere(pt, 2)


def test_prism():
    pass


def test_cone():
    pt = Point(0, 0, 0)
    dir = Direction(0, 0, 1)
    axis = Axis2(pt, dir)
    Cone(axis, 2, 0.5, 5)
