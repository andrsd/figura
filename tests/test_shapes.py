import math

import pytest
from figura.shapes import (
    Point,
    Wire,
    Face,
    Edge,
    Line,
    Circle,
    ArcOfCircle,
    Polygon,
    Spline
)
from figura.geometry import (
    Vector,
    Geometry,
    Axis1,
    Direction
)
from figura.primitives import (
    Box
)
from figura.oper import *

from OCC.Core.gp import (
    gp_Pnt
)


def test_point():
    pt = Point(1, 2, 3)
    pt.name = "pt1"
    assert pt.name == "pt1"

    assert pt.x == 1
    assert pt.y == 2
    assert pt.z == 3
    assert pt.is_equal(Point(1, 2, 3), 1e-15)

    s = str(pt)
    assert s == "<class 'figura.shapes.Point'>(x=1.0, y=2.0, z=3.0)"

    gp = gp_Pnt(3, 2, 1)
    p = Point.from_pnt(gp)
    assert p.x == 3
    assert p.y == 2
    assert p.z == 1


def test_line():
    v1 = Point(0, 0, 0)
    v2 = Point(1, 0, 0)
    ln = Line(v1, v2)
    assert math.isclose(ln.length(), 1., rel_tol=1e-10)


def test_wire():
    v1 = Point(0, 0, 0)
    v2 = Point(1, 0, 0)
    v3 = Point(2, 0, 0)
    edge1 = Line(v1, v2)
    edge2 = Line(v2, v3)
    Wire([edge1, edge2])


def test_face():
    v1 = Point(0, 0, 0)
    v2 = Point(1, 0, 0)
    v3 = Point(1, 2, 0)
    edge1 = Line(v1, v2)
    edge2 = Line(v2, v3)
    edge3 = Line(v3, v1)
    wire = Wire([edge1, edge2, edge3])
    face = Face(wire)
    assert math.isclose(face.area(), 1., rel_tol=1e-10)


def test_mirror():
    pt1 = Point(0, 1, 0)

    x_axis = Geometry.OX()
    pt1.mirror(x_axis)


def test_fuse():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 4, 1)
    box1 = Box(pt1, pt2)

    pt3 = Point(1, 1, 0)
    pt4 = Point(3, 3, 1)
    tool = Box(pt3, pt4)

    box1.fuse(tool)
    fuse(box1, tool)


def test_fuse_wrong_tool_type():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 1)
    box1 = Box(pt1, pt2)

    with pytest.raises(TypeError):
        box1.cut(Geometry.OX())


def test_cut():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 1)
    box1 = Box(pt1, pt2)

    pt3 = Point(0.5, 0.5, 1)
    tool = Box(pt1, pt3)

    box1.cut(tool)
    cut(box1, tool)


def test_cut_wrong_tool_type():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 1)
    box1 = Box(pt1, pt2)

    with pytest.raises(TypeError):
        box1.cut(Geometry.OX())


def test_intersect():
    pt1 = Point(-0.5, -0.5, 0)
    pt2 = Point(1, 1, 1)
    box1 = Box(pt1, pt2)

    pt3 = Point(-1, -1, 0)
    pt4 = Point(0.5, 0.5, 1)
    tool = Box(pt3, pt4)

    box1.intersect(tool)
    intersect(box1, tool)


def test_intersect_wrong_tool_type():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 1)
    box1 = Box(pt1, pt2)

    with pytest.raises(TypeError):
        box1.intersect(Geometry.OX())


def test_edges():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 1)
    box = Box(pt1, pt2)

    edges = box.edges()
    assert len(edges) == 24


def test_faces():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 1)
    box = Box(pt1, pt2)

    faces = box.faces()
    assert len(faces) == 6


def test_fillet():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 1)
    box = Box(pt1, pt2)

    edges = box.edges()
    box.fillet(edges, 0.1)
    fillet(box, edges, 0.1)


def test_hollow():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 1)
    box = Box(pt1, pt2)

    face = box.faces()[0]
    box.hollow([face], 0.1, 1e-3)
    hollow(box, [face], 0.1, 1e-3)


def test_plane():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 1)
    box = Box(pt1, pt2)

    face = box.faces()[0]
    assert face.is_plane()
    plane = face.plane()
    assert plane.location.x == 0
    assert plane.location.y == 0
    assert plane.location.z == 0


def test_extrude():
    pt1 = Point(0, 0, 0)
    vec = Vector(1, 0, 0)
    pt1.extrude(vec)
    extrude(pt1, vec)


def test_revolve():
    pt1 = Point(1, -0.5, 0)
    pt2 = Point(1, 0.5, 0)
    edge = Line(pt1, pt2)
    oz = Geometry.OZ()
    edge.revolve(oz)
    revolve(edge, oz)


def test_translate_vec():
    pt1 = Point(1, -0.5, 0)
    pt2 = Point(1, 0.5, 0)
    edge = Line(pt1, pt2)
    m = edge.translate(Vector(-1, 0, 0))


def test_translate_2pts():
    pt1 = Point(1, -0.5, 0)
    pt2 = Point(1, 0.5, 0)
    edge = Line(pt1, pt2)
    m = edge.translate(Point(1, 1, 0), Point(-1, 2, 0))


def test_scale():
    pt1 = Point(1, -0.5, 0)
    pt2 = Point(1, 0.5, 0)
    edge = Line(pt1, pt2)
    m = edge.scale(0.25)


def test_rotate_point():
    pt1 = Point(-1, 0., 0)
    ax1 = Axis1(Point(0, 0, 0), Direction(0, 0, -1))
    pt2 = pt1.rotate(ax1, 90)
    assert math.isclose(pt2.x, 0., abs_tol=1e-10)
    assert math.isclose(pt2.y, 1., abs_tol=1e-10)
    assert math.isclose(pt2.z, 0., abs_tol=1e-10)


def test_rotate():
    pt1 = Point(1, -0.5, 0)
    pt2 = Point(1, 0.5, 0)
    ax1 = Axis1(pt1, Direction(0, 0, 1))
    edge = Line(pt1, pt2)
    m = edge.rotate(ax1, 90)
    assert isinstance(m, Edge)


def test_circle_center_radius():
    ctr = Point(1, 2, 3)
    circ = Circle(ctr, 1.)
    assert circ.radius == 1.
    assert circ.area == math.pi
    assert circ.location.is_equal(Point(1, 2, 3))
    assert math.isclose(circ.length(), 2. * math.pi, rel_tol=1e-10)


def test_circle_center_point():
    ctr = Point(0, 0, 0)
    circ = Circle(ctr, Point(1, 0, 0))
    assert circ.radius == 1.
    assert circ.area == math.pi
    assert circ.location.is_equal(Point(0, 0, 0))
    assert math.isclose(circ.length(), 2. * math.pi, rel_tol=1e-10)


def test_circle_3pt_point():
    circ = Circle(Point(1, 0, 0), Point(0, 1, 0), Point(-1, 0, 0))
    assert circ.radius == 1.
    assert circ.location.is_equal(Point(0, 0, 0))
    assert circ.area == math.pi
    assert math.isclose(circ.length(), 2. * math.pi, rel_tol=1e-10)


def test_arcofcircle_3pt():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 0)
    pt3 = Point(2, 0, 0)
    arc = ArcOfCircle(pt1, pt2, pt3)
    assert arc.start_point.is_equal(Point(0, 0, 0))
    assert arc.end_point.is_equal(Point(2, 0, 0))
    assert math.isclose(arc.length(), math.pi, rel_tol=1e-10)


def test_arcofcircle_center():
    pt1 = Point(1, 0, 0)
    pt2 = Point(0, 1, 0)
    ctr = Point(0, 0, 0)
    arc = ArcOfCircle(pt1, pt2, center=ctr)
    assert arc.start_point.is_equal(Point(1, 0, 0))
    assert arc.end_point.is_equal(Point(0, 1, 0))


def test_arcofcircle_tang():
    pt1 = Point(1, 0, 0)
    pt2 = Point(0, 1, 0)
    tg = Vector(1, 0, 0)
    arc = ArcOfCircle(pt2, tg, pt1)
    assert arc.start_point.is_equal(Point(0, 1, 0))
    assert arc.end_point.is_equal(Point(1, 0, 0))


def test_color():
    box = Box(Point(0, 0, 0), Point(1, 2, 3))
    box.color = (127.5, 127.5, 127.5)
    assert box.color == [0.5, 0.5, 0.5]

    box.color = [127.5, 127.5, 127.5]
    assert box.color == [0.5, 0.5, 0.5]


def test_color_error():
    box = Box(Point(0, 0, 0), Point(1, 2, 3))
    with pytest.raises(TypeError):
        box.color = 1


def test_polygon():
    pts = [
        Point(1, 0, 0),
        Point(0, 1, 0),
        Point(-1, 0, 0)
    ]
    poly = Polygon(pts)
    assert isinstance(poly.edge(), Edge)
    assert isinstance(poly.wire(), Wire)


def test_polygon_not_enough_points():
    pts = [
        Point(1, 0, 0)
    ]
    with pytest.raises(SystemExit):
        Polygon(pts)


def test_polygon_wrong_args():
    pts = 1.
    with pytest.raises(TypeError):
        Polygon(pts)


def test_spline():
    pts = [
        Point(0, 0.5, 0),
        Point(1, 0, 0),
        Point(4, 1, 0)
    ]
    tg = Vector(1, 0, 0)
    spline = Spline(pts, initial_tangent=tg, final_tangent=-tg)
    assert isinstance(spline, Edge)
    assert math.isclose(spline.length(), 4.42384280405, rel_tol=1e-10)
