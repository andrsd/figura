from OCC.Core.gp import (gp_Pnt2d)
from OCC.Core.TopoDS import (
    TopoDS_Shape,
)


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
