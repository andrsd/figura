import math
from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepBuilderAPI import (
    BRepBuilderAPI_MakeVertex,
    BRepBuilderAPI_MakeEdge,
    BRepBuilderAPI_MakeWire,
    BRepBuilderAPI_MakeFace,
    BRepBuilderAPI_MakeShell,
    BRepBuilderAPI_MakeSolid,
    BRepBuilderAPI_MakePolygon
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
    BRepPrimAPI_MakePrism,
    BRepPrimAPI_MakeRevol
)
from OCC.Core.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCC.Core.GeomAbs import GeomAbs_Plane
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.TopoDS import topods
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_FACE
from OCC.Core.TopTools import TopTools_ListOfShape
from OCC.Core.GC import (
    GC_MakeCircle,
    GC_MakeArcOfCircle
)
import figura
# from .geometry import (
#     Plane,
#     Axis1,
#     Direction
# )
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

    def mirror(self, axis):
        op = figura.transformations.Mirror(axis)
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

    def revolve(self, axis, angle=2.*math.pi):
        if isinstance(axis, figura.geometry.Axis1):
            rev = BRepPrimAPI_MakeRevol(self._shape, axis.obj(), angle)
            rev.Build()
            if not rev.IsDone():
                raise SystemExit("revolve failed")  # pragma: no cover
            return Shape.from_obj(rev.Shape())
        else:
            raise TypeError("Wrong argument types")

    @classmethod
    def from_obj(cls, obj):
        return cls(obj)


class Point(Shape):
    """
    Point
    """

    def __init__(self, x=None, y=None, z=None):
        super().__init__()
        if isinstance(x, TopoDS_Vertex):
            self._pnt = None
            self._shape = x
        elif isinstance(x, gp_Pnt):
            self._pnt = x
            vertex = BRepBuilderAPI_MakeVertex(self._pnt)
            vertex.Build()
            if not vertex.IsDone():
                raise SystemExit("Point was not created")  # pragma: no cover
            self._shape = vertex.Vertex()
        elif x is not None and y is not None and z is not None:
            self._pnt = gp_Pnt(x, y, z)
            vertex = BRepBuilderAPI_MakeVertex(self._pnt)
            vertex.Build()
            if not vertex.IsDone():
                raise SystemExit("Point was not created")  # pragma: no cover
            self._shape = vertex.Vertex()
        else:
            raise TypeError("Wrong argument types")

    def pnt(self):
        return self._pnt

    @property
    def x(self):
        """
        X-coordinate of this point
        """
        return self._pnt.X()

    @property
    def y(self):
        """
        Y-coordinate of this point
        """
        return self._pnt.Y()

    @property
    def z(self):
        """
        Z-coordinate of this point
        """
        return self._pnt.Z()

    def __str__(self):
        return "{}(x={}, y={}, z={})".format(
            self.__class__, self.x, self.y, self.z)

    @classmethod
    def from_obj(cls, obj):
        return cls(obj)


class Edge(Shape):

    def __init__(self, arg1=None):
        super().__init__()
        if isinstance(arg1, TopoDS_Edge):
            self._shape = arg1

    def _build_edge(self, edge):
        edge.Build()
        if not edge.IsDone():
            raise SystemExit("Edge was not created")  # pragma: no cover
        return edge.Edge()

    @classmethod
    def from_obj(cls, obj):
        return cls(obj)


class Line(Edge):

    def __init__(self, pt1, pt2):
        super().__init__()
        if isinstance(pt1, Point) and isinstance(pt2, Point):
            self._shape = self._build_edge(BRepBuilderAPI_MakeEdge(pt1.pnt(), pt2.pnt()))
        else:
            raise TypeError("Wrong argument types")


class Circle(Edge):

    def __init__(self, center, radius, norm=figura.geometry.Direction(0, 0, 1)):
        super().__init__()
        mk = GC_MakeCircle(center.pnt(), norm.obj(), radius)
        if not mk.IsDone():
            raise SystemExit("Circle was not created")  # pragma: no cover
        self._shape = self._build_edge(BRepBuilderAPI_MakeEdge(mk.Value()))


class ArcOfCircle(Edge):

    def __init__(self, pt1, pt2, pt3):
        super().__init__()
        mk = GC_MakeArcOfCircle(pt1.pnt(), pt2.pnt(), pt3.pnt())
        if not mk.IsDone():
            raise SystemExit("ArcOfCircle was not created")  # pragma: no cover
        self._shape = self._build_edge(BRepBuilderAPI_MakeEdge(mk.Value()))


class Wire(Shape):

    def __init__(self, arg1):
        super().__init__()
        if isinstance(arg1, list):
            wire = BRepBuilderAPI_MakeWire()
            for item in arg1:
                if isinstance(item, Edge) or isinstance(item, Wire):
                    wire.Add(item.shape())
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
            face = BRepBuilderAPI_MakeFace(arg1.shape())
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
        return figura.geometry.Plane.from_obj(BRepAdaptor_Surface(self._shape, True).Plane())

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
                solid.Add(sh.shape())
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


class Polygon(Shape):

    def __init__(self, arg1, closed=True):
        if isinstance(arg1, list):
            if len(arg1) < 3:
                raise SystemExit("Polygon needs at least 3 points")
            self._polygon = BRepBuilderAPI_MakePolygon()
            for item in arg1:
                if isinstance(item, Point):
                    self._polygon.Add(item.shape())
            if closed:
                self._polygon.Close()
            self._polygon.Build()
            if not self._polygon.IsDone():
                raise SystemExit("Polygon was not created")  # pragma: no cover
            super().__init__(shape=self._polygon.Shape())
        else:
            raise TypeError("Wrong argument types")

    def edge(self):
        return Edge.from_obj(self._polygon.Edge())

    def wire(self):
        return Wire.from_obj(self._polygon.Wire())

    @classmethod
    def from_obj(cls, obj):
        return cls(obj)
