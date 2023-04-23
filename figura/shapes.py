import math
from OCC.Core.gp import (gp_Pnt, gp_Trsf)
from OCC.Core.BRepBuilderAPI import (
    BRepBuilderAPI_MakeVertex,
    BRepBuilderAPI_MakeEdge,
    BRepBuilderAPI_MakeWire,
    BRepBuilderAPI_MakeFace,
    BRepBuilderAPI_MakeShell,
    BRepBuilderAPI_MakeSolid,
    BRepBuilderAPI_MakePolygon,
    BRepBuilderAPI_Transform
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
from .geometry import Axis1


class Shape(object):

    def __init__(self, shape=None):
        self._name = None
        self._color = None
        if shape is not None and isinstance(shape, TopoDS_Shape):
            self._shape = shape
        elif shape is None:
            self._shape = shape
        else:
            raise TypeError("Wrong argument types")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str):
            self._name = value
        else:
            raise TypeError("'value' must be a 'string'.")

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if isinstance(value, list) and len(value) == 3:
            self._color = value
        elif isinstance(value, tuple) and len(value) == 3:
            self._color = [value[0], value[1], value[2]]
        else:
            raise TypeError("'value' must be a list with 3 elements: [r, g, b].")
        self._color = [val / 255. for val in self._color]

    def shape(self):
        return self._shape

    def mirror(self, axis):
        if isinstance(axis, Axis1):
            trsf = gp_Trsf()
            trsf.SetMirror(axis.ax1())
            brep_trsf = BRepBuilderAPI_Transform(self.shape(), trsf)
            return self.__class__.from_shape(brep_trsf.Shape())
        else:
            raise SystemError("axis must be 'Axis1'")

    def fuse(self, shape):
        if hasattr(shape, 'shape'):
            fuse = BRepAlgoAPI_Fuse(self.shape(), shape.shape())
            fuse.Build()
            if not fuse.IsDone():
                raise SystemExit("Objects were not fused")  # pragma: no cover
            return Shape.from_shape(fuse.Shape())
        else:
            raise TypeError("`shape` object does not have `shape()` method")

    def cut(self, tool):
        if hasattr(tool, 'shape'):
            cut = BRepAlgoAPI_Cut(self.shape(), tool.shape())
            cut.Build()
            if not cut.IsDone():
                raise SystemExit("Object was not cut")  # pragma: no cover
            return Shape.from_shape(cut.Shape())
        else:
            raise TypeError("`tool` object does not have `shape()` method")

    def intersect(self, tool):
        if hasattr(tool, 'shape'):
            isect = BRepAlgoAPI_Common(self.shape(), tool.shape())
            isect.Build()
            if not isect.IsDone():
                raise SystemExit("Object was not intersected")  # pragma: no cover
            return Shape.from_shape(isect.Shape())
        else:
            raise TypeError("`tool` object does not have `shape()` method")

    def edges(self):
        exp = TopExp_Explorer(self.shape(), TopAbs_EDGE)
        edgs = []
        while exp.More():
            e = exp.Current()
            edgs.append(Edge.from_shape(e))
            exp.Next()
        return edgs

    def faces(self):
        exp = TopExp_Explorer(self.shape(), TopAbs_FACE)
        fcs = []
        while exp.More():
            f = exp.Current()
            fcs.append(Face.from_shape(topods.Face(f)))
            exp.Next()
        return fcs

    def fillet(self, edges, radius):
        fillet = BRepFilletAPI_MakeFillet(self.shape())
        for e in edges:
            fillet.Add(radius, e.shape())
        return Shape.from_shape(fillet.Shape())

    def hollow(self, faces_to_remove, thickness, tolerance):
        # TODO: check that `faces_to_remove` is a iterable object
        rem_faces = TopTools_ListOfShape()
        for face in faces_to_remove:
            if isinstance(face, Face):
                rem_faces.Append(face.shape())

        thick_solid = BRepOffsetAPI_MakeThickSolid()
        thick_solid.MakeThickSolidByJoin(self._shape, rem_faces, thickness, tolerance)
        thick_solid.Build()
        return Shape.from_shape(thick_solid.Shape())

    def extrude(self, vec):
        prism = BRepPrimAPI_MakePrism(self._shape, vec.vec())
        prism.Build()
        if not prism.IsDone():
            raise SystemExit("extrude failed")  # pragma: no cover
        return Shape.from_shape(prism.Shape())

    def revolve(self, axis, angle=2.*math.pi):
        if isinstance(axis, figura.geometry.Axis1):
            rev = BRepPrimAPI_MakeRevol(self._shape, axis.ax1(), angle)
            rev.Build()
            if not rev.IsDone():
                raise SystemExit("revolve failed")  # pragma: no cover
            return Shape.from_shape(rev.Shape())
        else:
            raise TypeError("Wrong argument types")

    @classmethod
    def from_shape(cls, obj):
        return cls(obj)


class Point(Shape):
    """
    Defines a 3D cartesian point
    """

    def __init__(self, x, y, z):
        """
        Creates a point with its 3 cartesian coordinates

        :param x: x-coordinate
        :param y: y-coordinate
        :param z: z-coordinate
        """
        super().__init__()
        self._pnt = gp_Pnt(x, y, z)
        vertex = BRepBuilderAPI_MakeVertex(self._pnt)
        vertex.Build()
        if not vertex.IsDone():
            raise SystemExit("Point was not created")  # pragma: no cover
        self._shape = vertex.Vertex()

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
    def from_pnt(cls, pnt):
        if isinstance(pnt, gp_Pnt):
            return cls(pnt.X(), pnt.Y(), pnt.Z())
        else:
            raise TypeError("Argument 'pnt' must be of 'gp_Pnt' type")

    @classmethod
    def from_shape(cls, vertex):
        if isinstance(vertex, TopoDS_Vertex):
            cls._pnt = None
            cls._shape = vertex
            return cls
        else:
            raise TypeError("Argument 'vertex' must be of 'TopoDS_Vertex' type")


class Edge(Shape):

    def __init__(self, shape=None):
        super().__init__(shape)

    def _build_edge(self, edge):
        edge.Build()
        if not edge.IsDone():
            raise SystemExit("Edge was not created")  # pragma: no cover
        self._shape = edge.Edge()

    @classmethod
    def from_shape(cls, edge):
        if isinstance(edge, TopoDS_Edge):
            new = cls(shape=edge)
            return new
        else:
            raise TypeError("Argument 'edge' must be of 'TopoDS_Edge' type")


class Line(Edge):

    def __init__(self, pt1, pt2):
        super().__init__()
        if isinstance(pt1, Point) and isinstance(pt2, Point):
            self._build_edge(BRepBuilderAPI_MakeEdge(pt1.pnt(), pt2.pnt()))
        else:
            raise TypeError("Wrong argument types")


class Circle(Edge):

    def __init__(self, center, radius, norm=figura.geometry.Direction(0, 0, 1)):
        super().__init__()
        mk = GC_MakeCircle(center.pnt(), norm.dir(), radius)
        if not mk.IsDone():
            raise SystemExit("Circle was not created")  # pragma: no cover
        self._build_edge(BRepBuilderAPI_MakeEdge(mk.Value()))


class ArcOfCircle(Edge):

    def __init__(self, pt1, pt2, pt3):
        super().__init__()
        mk = GC_MakeArcOfCircle(pt1.pnt(), pt2.pnt(), pt3.pnt())
        if not mk.IsDone():
            raise SystemExit("ArcOfCircle was not created")  # pragma: no cover
        self._build_edge(BRepBuilderAPI_MakeEdge(mk.Value()))


class Wire(Shape):

    def __init__(self, edges=[], shape=None):
        if isinstance(edges, list):
            if len(edges) > 0:
                wire = BRepBuilderAPI_MakeWire()
                for item in edges:
                    if isinstance(item, Edge) or isinstance(item, Wire):
                        wire.Add(item.shape())
                wire.Build()
                if not wire.IsDone():
                    raise SystemExit("Wire was not created")  # pragma: no cover
                super().__init__(shape=wire.Wire())
            else:
                super().__init__(shape=shape)
        else:
            raise TypeError("Argument 'edges' must be a list of 'Edges'")

    @classmethod
    def from_shape(cls, wire):
        if isinstance(wire, TopoDS_Wire):
            new = cls()
            new._shape = wire
            return new
        else:
            raise TypeError("Argument 'wire' must be of 'TopoDS_Wire' type")


class Face(Shape):

    def __init__(self, wire=None, shape=None):
        if wire is None:
            super().__init__(shape=shape)
        elif isinstance(wire, Wire):
            wire = BRepBuilderAPI_MakeFace(wire.shape())
            wire.Build()
            if not wire.IsDone():
                raise SystemExit("Face was not created")  # pragma: no cover
            super().__init__(shape=wire.Face())
        else:
            raise TypeError("Wrong argument types")

    def is_plane(self):
        surf = BRepAdaptor_Surface(self._shape, True)
        surf_type = surf.GetType()
        return surf_type == GeomAbs_Plane

    def plane(self):
        pln = BRepAdaptor_Surface(self._shape, True).Plane()
        return figura.geometry.Plane.from_pln(pln)

    @classmethod
    def from_shape(cls, face):
        if isinstance(face, TopoDS_Face):
            new = cls()
            new._shape = face
            return new
        else:
            raise TypeError("Argument 'face' must be of 'TopoDS_Face' type")


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
    def from_shape(cls, obj):
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
    def from_shape(cls, obj):
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
        return Edge.from_shape(self._polygon.Edge())

    def wire(self):
        return Wire.from_shape(self._polygon.Wire())

    @classmethod
    def from_shape(cls, obj):
        return cls(obj)
