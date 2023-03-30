import pytest
from figura.shapes import (
    Vertex,
    Wire,
    Face,
    Line,
    Circle,
    ArcOfCircle
)
from figura.geometry import (
    Point,
    Vector,
    Geometry
)
from figura.primitives import (
    Box
)


def test_vertex():
    v = Vertex(1, 2, 3)
    v.name("pt1")
    assert v.name() == "pt1"


def test_line():
    v1 = Vertex(0, 0, 0)
    v2 = Vertex(1, 0, 0)
    Line(v1, v2)


def test_wire():
    v1 = Vertex(0, 0, 0)
    v2 = Vertex(1, 0, 0)
    v3 = Vertex(2, 0, 0)
    edge1 = Line(v1, v2)
    edge2 = Line(v2, v3)
    Wire([edge1, edge2])


def test_face():
    v1 = Vertex(0, 0, 0)
    v2 = Vertex(1, 0, 0)
    v3 = Vertex(2, 0, 0)
    edge1 = Line(v1, v2)
    edge2 = Line(v2, v3)
    edge3 = Line(v3, v1)
    wire = Wire([edge1, edge2, edge3])
    Face(wire)


def test_mirror():
    pt1 = Vertex(0, 1, 0)

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


def test_fuse_wrong_tool_type():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 1)
    box1 = Box(pt1, pt2)

    with pytest.raises(TypeError):
        box1.cut(Point(1, 1, 1))


def test_cut():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 1)
    box1 = Box(pt1, pt2)

    pt3 = Point(0.5, 0.5, 1)
    tool = Box(pt1, pt3)

    box1.cut(tool)


def test_cut_wrong_tool_type():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 1)
    box1 = Box(pt1, pt2)

    with pytest.raises(TypeError):
        box1.cut(Point(1, 1, 1))


def test_intersect():
    pt1 = Point(-0.5, -0.5, 0)
    pt2 = Point(1, 1, 1)
    box1 = Box(pt1, pt2)

    pt3 = Point(-1, -1, 0)
    pt4 = Point(0.5, 0.5, 1)
    tool = Box(pt3, pt4)

    box1.intersect(tool)


def test_intersect_wrong_tool_type():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 1)
    box1 = Box(pt1, pt2)

    with pytest.raises(TypeError):
        box1.intersect(Point(1, 1, 1))


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


def test_hollow():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 1)
    box = Box(pt1, pt2)

    face = box.faces()[0]
    box.hollow([face], 0.1, 1e-3)


def test_plane():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 1)
    box = Box(pt1, pt2)

    face = box.faces()[0]
    assert face.is_plane() == True
    plane = face.plane()
    assert plane.location.x == 0
    assert plane.location.y == 0
    assert plane.location.z == 0


def test_extrude():
    pt1 = Vertex(0, 0, 0)
    vec = Vector(1, 0, 0)
    pt1.extrude(vec)


def test_revolve():
    pt1 = Vertex(1, -0.5, 0)
    pt2 = Vertex(1, 0.5, 0)
    edge = Line(pt1, pt2)
    oz = Geometry.OZ()
    edge.revolve(oz)


def test_line_pt():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 0, 0)
    Line(pt1, pt2)


def test_circle():
    ctr = Point(0, 0, 0)
    Circle(ctr, 1.)


def test_arcofcircle():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 0)
    pt3 = Point(2, 0, 0)
    ArcOfCircle(pt1, pt2, pt3)
