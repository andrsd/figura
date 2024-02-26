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
