import pytest
from figura.shapes import (
    Point,
    Wire,
    Plane,
    Direction
)
from figura.primitives import (
    Box
)
from figura.oper import (
    section
)


def test_section():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 1)
    box = Box(pt1, pt2)
    pln = Plane(Point(0.5, 0., 0.), Direction(1., 1., 0.))
    wire = section(box, pln)
    assert(isinstance(wire, Wire))
