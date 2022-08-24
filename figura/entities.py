from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepBuilderAPI import (
    BRepBuilderAPI_MakeVertex,
    BRepBuilderAPI_MakeEdge,
    BRepBuilderAPI_MakeWire,
    BRepBuilderAPI_MakeFace,
    BRepBuilderAPI_MakeShell,
    BRepBuilderAPI_MakeSolid
)


class Entity(object):

    def __init__(self):
        self._name = None
        self._shape = None

    def name(self, value=None):
        if value is None:
            return self._name
        elif isinstance(value, str):
            self._name = value
        else:
            raise TypeError("'value' must be a 'string'.")

    def shape(self):
        return self._shape


class Vertex(Entity):
    """
    Vertex
    """

    def __init__(self, x, y, z):
        super().__init__()
        pt = gp_Pnt(x, y, z)
        vertex = BRepBuilderAPI_MakeVertex(pt)
        vertex.Build()
        if not vertex.IsDone():
            raise SystemExit("Vertex was not created")
        self._shape = vertex.Vertex()


class Edge(Entity):

    def __init__(self, v1, v2):
        super().__init__()
        if not isinstance(v1, Vertex):
            raise TypeError("'v1' must be a 'Vertex'")
        if not isinstance(v2, Vertex):
            raise TypeError("'v2' must be a 'Vertex'")

        edge = BRepBuilderAPI_MakeEdge(v1.shape(), v2.shape())
        edge.Build()
        if not edge.IsDone():
            raise SystemExit("Edge was not created")
        self._shape = edge.Edge()


class Wire(Entity):

    def __init__(self, edges):
        super().__init__()
        if not isinstance(edges, list):
            raise TypeError("'edges' must be a list of 'Edge's")
        wire = BRepBuilderAPI_MakeWire()
        for edg in edges:
            wire.Add(edg.shape())
        wire.Build()
        if not wire.IsDone():
            raise SystemExit("Wire was not created")
        self._shape = wire.Wire()


class Face(Entity):

    def __init__(self, wire):
        super().__init__()
        if not isinstance(wire, Wire):
            raise TypeError("'wire' must be a 'Wire'")
        face = BRepBuilderAPI_MakeFace(wire.shape())
        face.Build()
        if not face.IsDone():
            raise SystemExit("Face was not created")
        self._shape = face.Face()


class Shell(Entity):
    def __init__(self):
        raise NotImplementedError()
        super().__init__()
        shell = BRepBuilderAPI_MakeShell()
        shell.Build()
        if not shell.IsDone():
            raise SystemExit("Shell was not created")
        self._shape = shell.Shell()


class Solid(Entity):
    def __init__(self, shells):
        super().__init__()
        if not isinstance(shells, list):
            raise TypeError("'shells' must be a list of 'Shell's")
        solid = BRepBuilderAPI_MakeSolid()
        for sh in shells:
            solid.Add(sh.shape())
        solid.Build()
        if not solid.IsDone():
            raise SystemExit("Solid was not created")
        self._shape = solid.Solid()
