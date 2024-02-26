from multimethod import multimethod
from OCC.Core.gp import (
    gp_Pnt2d,
    gp_Circ2d,
)
from OCC.Core.BRepBuilderAPI import (
    BRepBuilderAPI_MakeEdge2d,
    BRepBuilderAPI_MakeWire,
    BRepBuilderAPI_MakeFace,
)
from OCC.Core.TopoDS import (
    TopoDS_Shape,
    TopoDS_Edge,
    TopoDS_Wire,
    TopoDS_Face,
)
from OCC.Core.GCE2d import (
    GCE2d_MakeArcOfCircle,
)
from ._geometry import (Axis, Direction)


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

    @classmethod
    def from_shape(cls, obj):
        return cls(obj)


class Point(Shape):
    """
    Defines a 3D cartesian point
    """

    def __init__(self, x, y):
        """
        Creates a point with its 2 cartesian coordinates

        :param x: x-coordinate
        :param y: y-coordinate
        """
        super().__init__()
        self._pnt = gp_Pnt2d(x, y)

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

    def __str__(self):
        return "{}(x={}, y={})".format(
            self.__class__, self.x, self.y)

    @classmethod
    def from_shape(cls, vertex):
        if isinstance(vertex, gp_Pnt2d):
            return cls(vertex.X(), vertex.Y())
        else:
            raise TypeError("Argument 'vertex' must be of 'gp_Pnt2d' type")

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
            self._build_edge(BRepBuilderAPI_MakeEdge2d(pt1.pnt(), pt2.pnt()))
        else:
            raise TypeError("Wrong argument types")


class Circle(Edge):
    """
    Describes a circle in 2D space. A circle is defined by its radius and
    position in space with a coordinate system.
    """

    @multimethod
    def __init__(self, center: Point, radius: float):
        """
        Construct a circle from a center point and a radius.

        :param center: Center point
        :param radius: Radius
        """
        super().__init__()
        ax = Axis(center, Direction(1, 0))
        self._circ = gp_Circ2d(ax.ax(), radius)
        self._build_edge(BRepBuilderAPI_MakeEdge2d(self._circ))

    @multimethod
    def __init__(self, center: Point, pt: Point):
        """
        Construct a circle from a center point and another point

        :param center: Center point
        :param pt: Point that is part of the circle
        """
        radius = center.pnt().Distance(pt.pnt())
        ax = Axis(center, Direction(1, 0))
        self._circ = gp_Circ2d(ax.ax(), radius)
        self._build_edge(BRepBuilderAPI_MakeEdge2d(self._circ))

    @property
    def area(self):
        return self._circ.Area()

    @property
    def radius(self):
        return self._circ.Radius()

    @property
    def location(self):
        pnt = self._circ.Location()
        return Point.from_shape(pnt)


class ArcOfCircle(Edge):
    """
    Describes an arc of a circle in 3D space.
    """

    @multimethod
    def __init__(self, pt1: Point, pt2: Point, pt3: Point = None, center: Point = None):
        super().__init__()
        self._arc = None
        if pt3 is not None and center is None:
            mk = GCE2d_MakeArcOfCircle(pt1.pnt(), pt2.pnt(), pt3.pnt())
            if not mk.IsDone():
                raise SystemExit("ArcOfCircle was not created")  # pragma: no cover
            self._build_edge(BRepBuilderAPI_MakeEdge2d(mk.Value()))
            self._arc = mk.Value()
        elif pt3 is None and center is not None:
            radius = center.pnt().Distance(pt1.pnt())
            ax = Axis(center, Direction(1, 0))
            circ = gp_Circ2d(ax.ax(), radius)
            mk = GCE2d_MakeArcOfCircle(circ, pt1.pnt(), pt2.pnt(), True)
            if not mk.IsDone():
                raise SystemExit("ArcOfCircle was not created")  # pragma: no cover
            self._build_edge(BRepBuilderAPI_MakeEdge2d(mk.Value()))
            self._arc = mk.Value()
        else:
            raise TypeError("Must specify either 'pt3' or 'center'.")

    @property
    def start_point(self):
        pnt = self._arc.StartPoint()
        return Point.from_shape(pnt)

    @property
    def end_point(self):
        pnt = self._arc.EndPoint()
        return Point.from_shape(pnt)


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

    @classmethod
    def from_shape(cls, face):
        if isinstance(face, TopoDS_Face):
            new = cls()
            new._shape = face
            return new
        else:
            raise TypeError("Argument 'face' must be of 'TopoDS_Face' type")
