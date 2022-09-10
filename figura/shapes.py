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
    BRepAlgoAPI_Fuse,
    BRepAlgoAPI_Cut,
    BRepAlgoAPI_Common
)
from OCC.Core.BRepOffsetAPI import (
    BRepOffsetAPI_MakeThickSolid
)
from OCC.Core.BRepPrimAPI import (
    BRepPrimAPI_MakePrism
)
from OCC.Core.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCC.Core.GeomAbs import GeomAbs_Plane
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.TopoDS import topods
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_FACE
from OCC.Core.TopTools import TopTools_ListOfShape
from .gc import GeoCurve
from .geometry import Plane
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

    def shape(self):
        return self._shape

    def obj(self):
        return self._shape

    def mirror(self, axis):
        op = Mirror(axis)
        return self.__class__.from_obj(op.do(self))

    def fuse(self, shape):
        if hasattr(shape, 'shape'):
            fuse = BRepAlgoAPI_Fuse(self.shape(), shape.shape())
            fuse.Build()
            if not fuse.IsDone():
                raise SystemExit("Objects were not fused")  # pragma: no cover
            return Shape.from_obj(fuse.Shape())
        else:
            raise TypeError("`shape` object does not have `shape()` method")

    def cut(self, tool):
        if hasattr(tool, 'shape'):
            cut = BRepAlgoAPI_Cut(self.shape(), tool.shape())
            cut.Build()
            if not cut.IsDone():
                raise SystemExit("Object was not cut")  # pragma: no cover
            return Shape.from_obj(cut.Shape())
        else:
            raise TypeError("`tool` object does not have `shape()` method")

    def intersect(self, tool):
        if hasattr(tool, 'shape'):
            isect = BRepAlgoAPI_Common(self.shape(), tool.shape())
            isect.Build()
            if not isect.IsDone():
                raise SystemExit("Object was not intersected")  # pragma: no cover
            return Shape.from_obj(isect.Shape())
        else:
            raise TypeError("`tool` object does not have `shape()` method")

    def edges(self):
        exp = TopExp_Explorer(self.shape(), TopAbs_EDGE)
        edgs = []
        while exp.More():
            e = exp.Current()
            edgs.append(Edge.from_obj(e))
            exp.Next()
        return edgs

    def faces(self):
        exp = TopExp_Explorer(self.shape(), TopAbs_FACE)
        fcs = []
        while exp.More():
            f = exp.Current()
            fcs.append(Face.from_obj(topods.Face(f)))
            exp.Next()
        return fcs

    def fillet(self, edges, radius):
        fillet = BRepFilletAPI_MakeFillet(self.shape())
        for e in edges:
            fillet.Add(radius, e.shape())
        return Shape.from_obj(fillet.Shape())

    def hollow(self, faces_to_remove, thickness, tolerance):
        # TODO: check that `faces_to_remove` is a iterable object
        rem_faces = TopTools_ListOfShape()
        for face in faces_to_remove:
            if isinstance(face, Face):
                rem_faces.Append(face.shape())

        thick_solid = BRepOffsetAPI_MakeThickSolid()
        thick_solid.MakeThickSolidByJoin(self._shape, rem_faces, thickness, tolerance)
        thick_solid.Build()
        return Shape.from_obj(thick_solid.Shape())

    def extrude(self, vec):
        prism = BRepPrimAPI_MakePrism(self._shape, vec.obj())
        prism.Build()
        if not prism.IsDone():
            raise SystemExit("extrude failed")  # pragma: no cover
        return Shape.from_obj(prism.Shape())

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
                raise SystemExit("Vertex was not created")  # pragma: no cover
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
                raise SystemExit("Edge was not created")  # pragma: no cover
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
                raise SystemExit("Wire was not created")  # pragma: no cover
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
                raise SystemExit("Face was not created")  # pragma: no cover
            self._shape = face.Face()
        elif isinstance(arg1, TopoDS_Face):
            self._shape = arg1
        else:
            raise TypeError("Wrong argument types")

    def is_plane(self):
        surf = BRepAdaptor_Surface(self._shape, True)
        surf_type = surf.GetType()
        return surf_type == GeomAbs_Plane

    def plane(self):
        return Plane.from_obj(BRepAdaptor_Surface(self._shape, True).Plane())

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
                raise SystemExit("Shell was not created")  # pragma: no cover
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
                raise SystemExit("Solid was not created")  # pragma: no cover
            self._shape = solid.Solid()
        elif isinstance(arg1, TopoDS_Solid):
            self._shape = arg1
        else:
            raise TypeError("Wrong argument types")

    @classmethod
    def from_obj(cls, obj):
        return cls(obj)
