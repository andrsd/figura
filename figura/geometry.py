from OCC.Core.gp import (
    gp_Vec,
    gp_Dir,
    gp_Ax1,
    gp_Ax2,
    gp_OX,
    gp_OY,
    gp_OZ,
    gp_DX,
    gp_DY,
    gp_DZ,
    gp_Pln
)
# from .shapes import Point
import figura


class Geometry(object):

    def __init__(self):
        self.shape = None

    @staticmethod
    def OX():
        ax1 = gp_OX()
        pt = figura.shapes.Point.from_obj(ax1.Location())
        direction = Direction.from_obj(ax1.Direction())
        return Axis1(pt, direction)

    @staticmethod
    def OY():
        ax1 = gp_OY()
        pt = figura.shapes.Point.from_obj(ax1.Location())
        direction = Direction.from_obj(ax1.Direction())
        return Axis1(pt, direction)

    @staticmethod
    def OZ():
        ax1 = gp_OZ()
        pt = figura.shapes.Point.from_obj(ax1.Location())
        direction = Direction.from_obj(ax1.Direction())
        return Axis1(pt, direction)

    @staticmethod
    def DX():
        direction = gp_DX()
        return Direction.from_obj(direction)

    @staticmethod
    def DY():
        direction = gp_DY()
        return Direction.from_obj(direction)

    @staticmethod
    def DZ():
        direction = gp_DZ()
        return Direction.from_obj(direction)


class Vector(object):
    """
    Non-persistent vector in 3D space
    """

    def __init__(self, x, y, z):
        self._vec = gp_Vec(x, y, z)

    @property
    def x(self):
        """
        X-coordinate of this vector
        """
        return self._vec.X()

    @property
    def y(self):
        """
        Y-coordinate of this vector
        """
        return self._vec.Y()

    @property
    def z(self):
        """
        Z-coordinate of this vector
        """
        return self._vec.Z()

    def obj(self):
        """
        Get the underlying OpenCascade object

        :return: The underlying OpenCascade object
        """
        return self._vec

    @classmethod
    def from_obj(cls, obj):
        """
        Construct ``figura`` object from an OpenCascade ``gp_Vec`` object

        :param obj: OpenCascade ``gp_Vec`` object
        :return: :class:`.Vector` object
        """
        return Vector(obj.X(), obj.Y(), obj.Z())

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    def __str__(self):
        return "{}(x={}, y={}, z={})".format(
            self.__class__, self.x, self.y, self.z)


class Direction(object):
    """
    Describes a unit vector in 3D space
    """

    def __init__(self, x, y, z):
        self._dir = gp_Dir(x, y, z)

    @property
    def x(self):
        """
        X-coordinate of this unit vector
        """
        return self._dir.X()

    @property
    def y(self):
        """
        Y-coordinate of this unit vector
        """
        return self._dir.Y()

    @property
    def z(self):
        """
        Z-coordinate of this unit vector
        """
        return self._dir.Z()

    def obj(self):
        """
        Get the underlying OpenCascade object

        :return: The underlying OpenCascade object
        """
        return self._dir

    @classmethod
    def from_obj(cls, obj):
        """
        Construct ``figura`` object from an OpenCascade ``gp_Dir`` object

        :param obj: OpenCascade ``gp_Dir`` object
        :return: :class:`.Direction` object
        """
        return Direction(obj.X(), obj.Y(), obj.Z())

    def __neg__(self):
        return Direction(-self.x, -self.y, -self.z)

    def __str__(self):
        return "{}(x={}, y={}, z={})".format(
            self.__class__, self.x, self.y, self.z)


class Axis1(object):

    def __init__(self, pt, direction):
        if not isinstance(pt, figura.shapes.Point):
            raise TypeError("'pt' must be a 'Point'")
        if not isinstance(direction, Direction):
            raise TypeError("'dir' must be a 'Direction'")
        self._location = pt
        self._direction = direction
        self._ax1 = gp_Ax1(pt.pnt(), direction.obj())

    @property
    def location(self):
        """
        Location of this axis
        """
        return self._location

    @property
    def direction(self):
        """
        Direction of this axis
        """
        return self._direction

    def obj(self):
        """
        Get the underlying OpenCascade object

        :return: The underlying OpenCascade object
        """
        return self._ax1


class Axis2(object):

    def __init__(self, pt, direction):
        if not isinstance(pt, figura.shapes.Point):
            raise TypeError("'pt' must be a 'Point'")
        if not isinstance(direction, Direction):
            raise TypeError("'dir' must be a 'Direction'")
        self._location = pt
        self._direction = direction
        self._ax2 = gp_Ax2(pt.pnt(), direction.obj())

    @property
    def location(self):
        """
        Location of this axis
        """
        return self._location

    @property
    def direction(self):
        """
        Direction of this axis
        """
        return self._direction

    def obj(self):
        """
        Get the underlying OpenCascade object

        :return: The underlying OpenCascade object
        """
        return self._ax2


class Plane(object):
    """
    Describes a plane

    A plane is positioned in space with a coordinate system (a gp_Ax3 object), such that the plane is defined by the
    origin, "X Direction" and "Y Direction" of this coordinate system, which is the "local coordinate system" of the
    plane. The "main Direction" of the coordinate system is a vector normal to the plane. It gives the plane an implicit
    orientation such that the plane is said to be "direct", if the coordinate system is right-handed, or "indirect" in
    the other case. Note: when a `gp_Pln` plane is converted into a `Geom_Plane` plane, some implicit properties of its
    local coordinate system are used explicitly:

    - its origin defines the origin of the two parameters of the planar surface,
    - its implicit orientation is also that of the Geom_Plane. See Also `gce_MakePln` which provides functions for more
      complex plane constructions, Geom_Plane which provides additional functions for constructing planes and works,
      in particular, with the parametric equations of planes
    """

    def __init__(self, pt, normal):
        """
        Construct a plane with location `pt` and normal direction `normal`

        :param pt: Point :py:class:`.Point`
        :param normal: Normal :py:class:`.Direction`
        """
        if isinstance(pt, figura.shapes.Point) and isinstance(normal, Direction):
            self._location = pt
            self._pln = gp_Pln(pt.pnt(), normal.obj())
        else:
            raise TypeError("Wrong argument types")

    @property
    def location(self):
        """
        Location of this plane
        """
        return self._location

    def obj(self):
        """
        Get the underlying OpenCascade object

        :return: The underlying OpenCascade object
        """
        return self._pln

    @classmethod
    def from_obj(cls, obj):
        """
        Construct ``figura`` object from an OpenCascade ``gp_Pln`` object

        :param obj: OpenCascade ``gp_Pln`` object
        :return: :class:`.Plane` object
        """
        pt = figura.shapes.Point.from_obj(obj.Location())
        normal = Direction.from_obj(obj.Axis().Direction())
        return Plane(pt, normal)
