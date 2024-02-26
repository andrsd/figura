import pytest
import math
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


def test_circle_center_radius_2d():
    ctr = Point(1, 2)
    circ = Circle(ctr, 1.)
    assert circ.radius == 1.
    assert circ.area == math.pi
    assert circ.location.is_equal(Point(1, 2))


def test_circle_center_point_2d():
    ctr = Point(0, 0)
    circ = Circle(ctr, Point(1, 0))
    assert circ.radius == 1.
    assert circ.area == math.pi
    assert circ.location.is_equal(Point(0, 0))


def test_arcofcircle_3pt_2d():
    pt1 = Point(0, 0)
    pt2 = Point(1, 1)
    pt3 = Point(2, 0)
    arc = ArcOfCircle(pt1, pt2, pt3)
    assert arc.start_point.is_equal(Point(0, 0))
    assert arc.end_point.is_equal(Point(2, 0))


def test_arcofcircle_center_2d():
    pt1 = Point(1, 0)
    pt2 = Point(0, 1)
    ctr = Point(0, 0)
    arc = ArcOfCircle(pt1, pt2, center=ctr)
    assert arc.start_point.is_equal(Point(1, 0))
    assert arc.end_point.is_equal(Point(0, 1))
