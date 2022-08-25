from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepBuilderAPI import (
    BRepBuilderAPI_MakeVertex,
    BRepBuilderAPI_MakeEdge,
    BRepBuilderAPI_MakeWire,
    BRepBuilderAPI_MakeFace,
    BRepBuilderAPI_MakeShell,
    BRepBuilderAPI_MakeSolid
)
from OCC.Core.TopoDS import (
    TopoDS_Shape,
    TopoDS_Vertex,
    TopoDS_Edge,
    TopoDS_Wire,
    TopoDS_Face,
    TopoDS_Shell,
    TopoDS_Solid
)
from OCC.Core.BRepAlgoAPI import (
    BRepAlgoAPI_Fuse
)
from .gc import GeoCurve
from .transformations import Mirror


class Shape(object):

    def __init__(self, shape=None):
        self._name = None
        if shape is not None and isinstance(shape, TopoDS_Shape):
            self._shape = shape
        elif shape is None:
            self._shape = shape
        else:
            raise TypeError("Wrong argument types")

    def name(self, value=None):
        if value is None:
            return self._name
        elif isinstance(value, str):
            self._name = value
        else:
            raise TypeError("'value' must be a 'string'.")

    def obj(self):
        return self._shape

    def mirror(self, axis):
        op = Mirror(axis)
        return self.__class__.from_obj(op.do(self))

    def fuse(self, shape):
        fuse = BRepAlgoAPI_Fuse(self.obj(), shape.obj())
        fuse.Build()
        if not fuse.IsDone():
            raise SystemExit("Objects were not fused")
        return Shape.from_obj(fuse.Shape())

    @classmethod
    def from_obj(cls, obj):
        return cls(obj)


class Vertex(Shape):
    """
    Vertex
    """

    def __init__(self, x=None, y=None, z=None):
        super().__init__()
        if isinstance(x, TopoDS_Vertex):
            self._shape = x
        elif x is not None and y is not None and z is not None:
            pt = gp_Pnt(x, y, z)
            vertex = BRepBuilderAPI_MakeVertex(pt)
            vertex.Build()
            if not vertex.IsDone():
                raise SystemExit("Vertex was not created")
            self._shape = vertex.Vertex()
        else:
            raise TypeError("Wrong argument types")

    @classmethod
    def from_obj(cls, obj):
        return cls(obj)


class Edge(Shape):

    def __init__(self, arg1=None, arg2=None):
        super().__init__()
        edge = None
        if isinstance(arg1, Vertex) and isinstance(arg2, Vertex):
            edge = BRepBuilderAPI_MakeEdge(arg1.obj(), arg2.obj())
        elif isinstance(arg1, GeoCurve):
            edge = BRepBuilderAPI_MakeEdge(arg1.obj())
        elif isinstance(arg1, TopoDS_Edge):
            self._shape = arg1
        else:
            raise TypeError("Wrong argument types")

        if edge is not None:
            edge.Build()
            if not edge.IsDone():
                raise SystemExit("Edge was not created")
            self._shape = edge.Edge()

    @classmethod
    def from_obj(cls, obj):
        return cls(obj)


class Wire(Shape):

    def __init__(self, arg1):
        super().__init__()
        if isinstance(arg1, list):
            wire = BRepBuilderAPI_MakeWire()
            for item in arg1:
                if isinstance(item, Edge) or isinstance(item, Wire):
                    wire.Add(item.obj())
            wire.Build()
            if not wire.IsDone():
                raise SystemExit("Wire was not created")
            self._shape = wire.Wire()
        elif isinstance(arg1, TopoDS_Wire):
            self._shape = arg1
        else:
            raise TypeError("Wrong argument types")

    @classmethod
    def from_obj(cls, obj):
        return cls(obj)


class Face(Shape):

    def __init__(self, arg1):
        super().__init__()
        if isinstance(arg1, Wire):
            face = BRepBuilderAPI_MakeFace(arg1.obj())
            face.Build()
            if not face.IsDone():
                raise SystemExit("Face was not created")
            self._shape = face.Face()
        elif isinstance(arg1, TopoDS_Face):
            self._shape = arg1
        else:
            raise TypeError("Wrong argument types")

    @classmethod
    def from_obj(cls, obj):
        return cls(obj)


class Shell(Shape):

    def __init__(self, arg1):
        raise NotImplementedError()
        if isinstance(arg1, TopoDS_Shell):
            self._shape = arg1
        else:
            super().__init__()
            shell = BRepBuilderAPI_MakeShell()
            shell.Build()
            if not shell.IsDone():
                raise SystemExit("Shell was not created")
            self._shape = shell.Shell()

    @classmethod
    def from_obj(cls, obj):
        return cls(obj)


class Solid(Shape):

    def __init__(self, arg1):
        super().__init__()
        if isinstance(arg1, list):
            solid = BRepBuilderAPI_MakeSolid()
            for sh in arg1:
                solid.Add(sh.obj())
            solid.Build()
            if not solid.IsDone():
                raise SystemExit("Solid was not created")
            self._shape = solid.Solid()
        elif isinstance(arg1, TopoDS_Solid):
            self._shape = arg1
        else:
            raise TypeError("Wrong argument types")

    @classmethod
    def from_obj(cls, obj):
        return cls(obj)
