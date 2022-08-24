import pytest
from figura.entities import (
    Vertex,
    Edge,
    Wire,
    Face,
    Shell,
    Solid
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
