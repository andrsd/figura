import pytest
from figura.gc import (
    Segment,
    ArcOfCircle
)
from figura.geometry import (
    Point
)
from OCC.Core.Geom import (
    Geom_TrimmedCurve
)

def test_segment():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 0, 0)
    seg = Segment(pt1, pt2)

    assert isinstance(seg.obj(), Geom_TrimmedCurve)


def test_arcofcircle():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 0)
    pt3 = Point(2, 0, 0)
    seg = ArcOfCircle(pt1, pt2, pt3)

    assert isinstance(seg.obj(), Geom_TrimmedCurve)
