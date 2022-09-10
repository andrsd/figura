import pytest
from figura.shapes import (
    Vertex,
    Edge,
    Wire,
    Face
)
from figura.geometry import (
    Point
)
from figura.primitives import (
    Box
)


def test_vertex():
    v = Vertex(1, 2, 3)
    v.name("pt1")
    assert v.name() == "pt1"


def test_edge():
    v1 = Vertex(0, 0, 0)
    v2 = Vertex(1, 0, 0)
    Edge(v1, v2)


def test_wire():
    v1 = Vertex(0, 0, 0)
    v2 = Vertex(1, 0, 0)
    v3 = Vertex(2, 0, 0)
    edge1 = Edge(v1, v2)
    edge2 = Edge(v2, v3)
    Wire([edge1, edge2])


def test_face():
    v1 = Vertex(0, 0, 0)
    v2 = Vertex(1, 0, 0)
    v3 = Vertex(2, 0, 0)
    edge1 = Edge(v1, v2)
    edge2 = Edge(v2, v3)
    edge3 = Edge(v3, v1)
    wire = Wire([edge1, edge2, edge3])
    Face(wire)


def test_cut():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 1)
    box1 = Box(pt1, pt2)

    pt3 = Point(0.5, 0.5, 1)
    tool = Box(pt1, pt3)

    res = box1.cut(tool)


def test_cut_wrong_tool_type():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 1)
    box1 = Box(pt1, pt2)

    with pytest.raises(TypeError):
        res = box1.cut(Point(1, 1, 1))
