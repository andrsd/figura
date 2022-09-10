import pytest
from figura.shapes import (
    Vertex,
    Edge,
    Face,
    Wire
)
from figura.geometry import (
    Point,
    Vector,
    Direction,
    Axis2
)
from figura.primitives import (
    Box,
    Cylinder,
    Sphere,
    Cone,
    Prism
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
    box = Box(pt1, pt2)
    shell = box.shell()


def test_cylinder():
    pt = Point(0, 0, 0)
    dir = Direction(0, 0, 1)
    axis = Axis2(pt, dir)
    cyl = Cylinder(axis, 0.5, 2)
    shell = cyl.shell()
    solid = cyl.solid()


def test_sphere():
    pt = Point(0, 0, 0)
    sph = Sphere(pt, 2)
    shell = sph.shell()
    solid = sph.solid()


def test_prism():
    pt1 = Vertex(0, 0, 0)
    pt2 = Vertex(1, 0, 0)
    pt3 = Vertex(0, 1, 0)
    edge1 = Edge(pt1, pt2)
    edge2 = Edge(pt2, pt3)
    edge3 = Edge(pt3, pt1)
    wire = Wire([edge1, edge2, edge3])
    face = Face(wire)
    vec = Vector(0, 0, 1)
    prism = Prism(face, vec)


def test_cone():
    pt = Point(0, 0, 0)
    dir = Direction(0, 0, 1)
    axis = Axis2(pt, dir)
    cone = Cone(axis, 2, 0.5, 5)
    shell = cone.shell()
    solid = cone.solid()
