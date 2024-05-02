import math
from multimethod import multimethod
from OCC.Core.gp import (gp_Pnt, gp_Trsf)
from OCC.Core.gce import (gce_MakePln)
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
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopoDS import topods
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_FACE
from OCC.Core.TopTools import TopTools_ListOfShape
from OCC.Core.GC import (
    GC_MakeCircle,
    GC_MakeArcOfCircle
)
from OCC.Core.GeomAPI import GeomAPI_Interpolate
from OCC.Core.TColgp import TColgp_HArray1OfPnt
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
from .geometry import (Axis1, Direction, Vector, Plane)


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
            fuse.SimplifyResult()
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
        if isinstance(axis, Axis1):
            rev = BRepPrimAPI_MakeRevol(self._shape, axis.ax1(), angle)
            rev.Build()
            if not rev.IsDone():
                raise SystemExit("revolve failed")  # pragma: no cover
            return Shape.from_shape(rev.Shape())
        else:
            raise TypeError("Wrong argument types")

    @multimethod
    def translate(self, v: Vector):
        if isinstance(v, Vector):
            trsf = gp_Trsf()
            trsf.SetTranslation(v.vec())
            brep_trsf = BRepBuilderAPI_Transform(self.shape(), trsf)
            return Shape.from_shape(brep_trsf.Shape())
        else:
            raise SystemError("v must be 'Vector'")

    @multimethod
    def translate(self, p1, p2):
        if isinstance(p1, Point) and isinstance(p2, Point):
            trsf = gp_Trsf()
            trsf.SetTranslation(p1.pnt(), p2.pnt())
            brep_trsf = BRepBuilderAPI_Transform(self.shape(), trsf)
            return Shape.from_shape(brep_trsf.Shape())
        else:
            raise SystemError("p1 and p2 must be 'Point'")

    def scale(self, s):
        if isinstance(s, float) or isinstance(s, int):
            trsf = gp_Trsf()
            trsf.SetScaleFactor(s)
            brep_trsf = BRepBuilderAPI_Transform(self.shape(), trsf)
            return Shape.from_shape(brep_trsf.Shape())
        else:
            raise SystemError("s must be a 'float' or an 'int'")

    def rotate(self, axis: Axis1, angle: float):
        """
        Rotate point about axis by an angle

        :param axis: Axis of rotation
        :param angle: Angle [in degrees]
        :return: Rotated shape
        """
        if isinstance(axis, Axis1) and (isinstance(angle, float) or isinstance(angle, int)):
            trsf = gp_Trsf()
            trsf.SetRotation(axis.ax1(), math.radians(angle))
            brep_trsf = BRepBuilderAPI_Transform(self.shape(), trsf)
            return self.__class__.from_shape(brep_trsf.Shape())
        else:
            raise SystemError("axis must be 'Axis1' and angle must a 'float' or an 'int'")

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
            pnt = BRep_Tool.Pnt(vertex)
            return cls(pnt.X(), pnt.Y(), pnt.Z())
        else:
            raise TypeError("Argument 'vertex' must be of 'TopoDS_Vertex' type")

    def is_equal(self, pt, tol=1e-15):
        if isinstance(pt, Point):
            return self._pnt.IsEqual(pt.pnt(), tol)
        else:
            raise TypeError("Argument 'pt' must be of 'Point' type")


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
            new = Edge(shape=edge)
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
    """
    Describes a circle in 3D space. A circle is defined by its radius and positioned in space with a coordinate system.
    """

    @multimethod
    def __init__(self, center: Point, radius: float, norm=Direction(0, 0, 1)):
        """
        Construct a circle from a center point and a radius.

        :param center: Center point
        :param radius: Radius
        :param norm: Normal of the plane
        """
        super().__init__()
        circ = GC_MakeCircle(center.pnt(), norm.dir(), radius)
        if not circ.IsDone():
            raise SystemExit("Circle was not created")  # pragma: no cover
        self._build_edge(BRepBuilderAPI_MakeEdge(circ.Value()))
        self._circ = circ.Value().Circ()

    @multimethod
    def __init__(self, center: Point, pt: Point, norm=Direction(0, 0, 1)):
        """
        Construct a circle from a center point and another point

        :param center: Center point
        :param pt: Point that is part of the circle
        :param norm: Normal of the plane
        """
        super().__init__()
        radius = center.pnt().Distance(pt.pnt())
        circ = GC_MakeCircle(center.pnt(), norm.dir(), radius)
        if not circ.IsDone():
            raise SystemExit("Circle was not created")  # pragma: no cover
        self._build_edge(BRepBuilderAPI_MakeEdge(circ.Value()))
        self._circ = circ.Value().Circ()

    @multimethod
    def __init__(self, pt1: Point, pt2: Point, pt3: Point):
        """
        Construct a circle from three points

        :param pt1: First point
        :param pt2: Second point
        :param pt3: Third point
        """
        super().__init__()
        circ = GC_MakeCircle(pt1.pnt(), pt2.pnt(), pt3.pnt())
        if not circ.IsDone():
            raise SystemExit("Circle was not created")  # pragma: no cover
        self._build_edge(BRepBuilderAPI_MakeEdge(circ.Value()))
        self._circ = circ.Value().Circ()

    @property
    def area(self):
        return self._circ.Area()

    @property
    def radius(self):
        return self._circ.Radius()

    @property
    def location(self):
        pnt = self._circ.Location()
        return Point.from_pnt(pnt)


class ArcOfCircle(Edge):
    """
    Describes an arc of a circle in 3D space.
    """

    @multimethod
    def __init__(self, pt1: Point, pt2: Point, pt3: Point = None, center: Point = None):
        super().__init__()
        self._arc = None
        if pt3 is not None and center is None:
            mk = GC_MakeArcOfCircle(pt1.pnt(), pt2.pnt(), pt3.pnt())
            if not mk.IsDone():
                raise SystemExit("ArcOfCircle was not created")  # pragma: no cover
            self._build_edge(BRepBuilderAPI_MakeEdge(mk.Value()))
            self._arc = mk.Value()
        elif pt3 is None and center is not None:
            radius = center.pnt().Distance(pt1.pnt())
            pln = gce_MakePln(center.pnt(), pt1.pnt(), pt2.pnt()).Value()
            ax2 = pln.Position().Ax2()
            circ = GC_MakeCircle(ax2, radius).Value().Circ()
            mk = GC_MakeArcOfCircle(circ, pt1.pnt(), pt2.pnt(), True)
            if not mk.IsDone():
                raise SystemExit("ArcOfCircle was not created")  # pragma: no cover
            self._build_edge(BRepBuilderAPI_MakeEdge(mk.Value()))
            self._arc = mk.Value()
        else:
            raise TypeError("Must specify either 'pt3' or 'center'.")

    @multimethod
    def __init__(self, pt1: Point, tangent: Vector, pt2: Point):
        """
        Construct an arc of a circle from a point, tangent at the point, and another point.

        :param pt1: First point
        :param tangent: Tangent at point `pt1`
        :param pt2: Second point
        """
        super().__init__()
        mk = GC_MakeArcOfCircle(pt1.pnt(), tangent.vec(), pt2.pnt())
        if not mk.IsDone():
            raise SystemExit("ArcOfCircle was not created")  # pragma: no cover
        self._build_edge(BRepBuilderAPI_MakeEdge(mk.Value()))
        self._arc = mk.Value()

    @property
    def start_point(self):
        pnt = self._arc.StartPoint()
        return Point.from_pnt(pnt)

    @property
    def end_point(self):
        pnt = self._arc.EndPoint()
        return Point.from_pnt(pnt)


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
        return Plane.from_pln(pln)

    def area(self):
        """
        Compute the surface area of the face

        :return: Surface area of the face
        """
        props = GProp_GProps()
        brepgprop.SurfaceProperties(self.shape(), props)
        return props.Mass()

    @classmethod
    def from_shape(cls, face):
        if isinstance(face, TopoDS_Face):
            new = cls()
            new._shape = face
            return new
        else:
            raise TypeError("Argument 'face' must be of 'TopoDS_Face' type")


class Shell(Shape):

    def __init__(self, shape=None):
        if isinstance(shape, TopoDS_Shell):
            super().__init__(shape=shape)
        else:
            raise TypeError("Argument 'shape' must be of 'TopoDS_Shell' type")

    @classmethod
    def from_shape(cls, obj):
        return cls(shape=obj)


class Solid(Shape):

    def __init__(self, shapes=None):
        if isinstance(shapes, TopoDS_Solid):
            super().__init__(shape=shapes)
        elif isinstance(shapes, list):
            solid = BRepBuilderAPI_MakeSolid()
            for sh in shapes:
                solid.Add(sh.shape())
            solid.Build()
            if not solid.IsDone():
                raise SystemExit("Solid was not created")  # pragma: no cover
            super().__init__(shape=solid.Solid())
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


class Spline(Edge):

    def __init__(self, points, initial_tangent=None, final_tangent=None):
        """
        Construct a B-spline that is passing through an array of points.
        If tangency is specified, the continuity will be C1. If not, then the
        continuity will be C2

        :param points: Array of :class:`.Vertex` s
        :param initial_tangent: Tangent (:class:`.Vector`) at the first node
        :param final_tangent: Tangent (:class:`.Vector`) at the last node
        """
        if isinstance(points, list):
            super().__init__()
            pnts = TColgp_HArray1OfPnt(1, len(points))
            for (idx, pt) in enumerate(points):
                pnts.SetValue(idx + 1, pt.pnt())
            mk = GeomAPI_Interpolate(pnts, False, 1e-8)
            if isinstance(initial_tangent, Vector) and \
               isinstance(final_tangent, Vector):
                final_tangent = -final_tangent
                mk.Load(initial_tangent.vec(), final_tangent.vec())
            mk.Perform()
            if not mk.IsDone():
                raise SystemExit("Spline was not created")  # pragma: no cover
            self._build_edge(BRepBuilderAPI_MakeEdge(mk.Curve()))
            self._spline = mk.Curve()
        else:
            raise TypeError("Wrong argument type")
