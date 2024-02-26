import pytest
from figura.d2 import *
from OCC.Core.gp import (
    gp_Pnt2d
)


def test_point_2d():
    pt = Point(1, 2)
    pt.name = "pt1"
    assert pt.name == "pt1"

    assert pt.x == 1
    assert pt.y == 2
    assert pt.is_equal(Point(1, 2), 1e-15)

    s = str(pt)
    assert s == "<class 'figura.d2._shapes.Point'>(x=1.0, y=2.0)"

    gp = gp_Pnt2d(3, 2)
    p = Point.from_shape(gp)
    assert p.x == 3
    assert p.y == 2


def test_line_2d():
    v1 = Point(0, 0)
    v2 = Point(1, 0)
    Line(v1, v2)


def test_wire_2d():
    v1 = Point(0, 0)
    v2 = Point(1, 0)
    v3 = Point(2, 0)
    edge1 = Line(v1, v2)
    edge2 = Line(v2, v3)
    Wire([edge1, edge2])


def test_face_2d():
    v1 = Point(0, 0)
    v2 = Point(1, 0)
    v3 = Point(2, 0)
    edge1 = Line(v1, v2)
    edge2 = Line(v2, v3)
    edge3 = Line(v3, v1)
    wire = Wire([edge1, edge2, edge3])
    Face(wire)
