from OCC.Core.gp import (
    gp_Vec,
    gp_Dir,
    gp_Ax1,
    gp_Ax2,
    gp_Pln
)
import figura


class Geometry(object):

    def __init__(self):
        self.shape = None

    @staticmethod
    def OX():
        pt = figura.shapes.Point(0, 0, 0)
        direction = Direction(1, 0, 0)
        return Axis1(pt, direction)

    @staticmethod
    def OY():
        pt = figura.shapes.Point(0, 0, 0)
        direction = Direction(0, 1, 0)
        return Axis1(pt, direction)

    @staticmethod
    def OZ():
        pt = figura.shapes.Point(0, 0, 0)
        direction = Direction(0, 0, 1)
        return Axis1(pt, direction)

    @staticmethod
    def DX():
        return Direction(1, 0, 0)

    @staticmethod
    def DY():
        return Direction(0, 1, 0)

    @staticmethod
    def DZ():
        return Direction(0, 0, 1)


class Vector(object):
    """
    Non-persistent vector in 3D space
    """

    def __init__(self, x, y, z):
        """
        Creates a point with its three cartesian coordinates.

        :param x: x-coordinate
        :param y: y-coordinate
        :param z: z-coordinate
        """
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

    def vec(self):
        """
        Get the underlying OpenCascade object

        :return: The underlying OpenCascade object
        """
        return self._vec

    @classmethod
    def from_vec(cls, vec):
        """
        Construct ``figura`` object from an OpenCascade ``gp_Vec`` object

        :param vec: OpenCascade ``gp_Vec`` object
        :return: :class:`.Vector` object
        """
        return Vector(vec.X(), vec.Y(), vec.Z())

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    def __str__(self):
        return "{}(x={}, y={}, z={})".format(
            self.__class__, self.x, self.y, self.z)


class Direction(object):
    """
    Describes a unit vector in 3D space. This unit vector is also called "Direction".
    """

    def __init__(self, x, y, z):
        """
        Creates a direction with its 3 cartesian coordinates.

        :param x: x-coordinate
        :param y: y-coordinate
        :param z: z-coordinate
        """
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

    def dir(self):
        """
        Get the underlying OpenCascade object

        :return: The underlying OpenCascade object
        """
        return self._dir

    @classmethod
    def from_dir(cls, dir):
        """
        Construct ``figura`` object from an OpenCascade ``gp_Dir`` object

        :param dir: OpenCascade ``gp_Dir`` object
        :return: :class:`.Direction` object
        """
        return Direction(dir.X(), dir.Y(), dir.Z())

    def __neg__(self):
        return Direction(-self.x, -self.y, -self.z)

    def __str__(self):
        return "{}(x={}, y={}, z={})".format(
            self.__class__, self.x, self.y, self.z)


class Axis1(object):

    def __init__(self, pt, direction):
        """
        Describes an axis in 3D space. An axis is defined by:

        - its origin (also referred to as its "Location point"), and
        - its unit vector (referred to as its "Direction" or "main Direction").

        An axis is used:

        - to describe 3D geometric entities (for example, the axis of a revolution entity). It serves the same purpose
          as the STEP function "axis placement one axis", or
        - to define geometric transformations (axis of symmetry, axis of rotation, and so on). For example, this entity
          can be used to locate a geometric entity or to define a symmetry axis.

        :param pt: :class:`.Point` the location point
        :param direction: :class:`.Direction` the direction of the axis
        """
        if not isinstance(pt, figura.shapes.Point):
            raise TypeError("'pt' must be a 'Point'")
        if not isinstance(direction, Direction):
            raise TypeError("'dir' must be a 'Direction'")
        self._location = pt
        self._direction = direction
        self._ax1 = gp_Ax1(pt.pnt(), direction.dir())

    @property
    def location(self):
        """
        Location of this axis as :class:`.Point`
        """
        return self._location

    @property
    def direction(self):
        """
        Direction of this axis as :class:`.Direction`
        """
        return self._direction

    def ax1(self):
        """
        Get the underlying OpenCascade object

        :return: The underlying OpenCascade object
        """
        return self._ax1


class Axis2(object):
    """
    Describes a right-handed coordinate system in 3D space. A coordinate system is defined by:

    - its origin (also referred to as its "Location point"), and
    - three orthogonal unit vectors, termed respectively the "X Direction", the "Y Direction" and the "Direction" (also
      referred to as the "main Direction"). The "Direction" of the coordinate system is called its "main Direction"
      because whenever this unit vector is modified, the "X Direction" and the "Y Direction" are recomputed. However,
      when we modify either the "X Direction" or the "Y Direction", "Direction" is not modified. The "main Direction" is
      also the "Z Direction". Since an Ax2 coordinate system is right-handed, its "main Direction" is always equal to
      the cross product of its "X Direction" and "Y Direction". To define a left-handed coordinate system, use `Axis3`.

    A coordinate system is used:

    - to describe geometric entities, in particular to position them. The local coordinate system of a geometric entity
      serves the same purpose as the STEP function "axis placement two axes", or
    - to define geometric transformations.

    Note: we refer to the "X Axis", "Y Axis" and "Z Axis", respectively, as to axes having:

    - the origin of the coordinate system as their origin, and
    - the unit vectors "X Direction", "Y Direction" and "main Direction", respectively, as their unit vectors. The
      "Z Axis" is also the "main Axis".
    """

    def __init__(self, pt, direction):
        if not isinstance(pt, figura.shapes.Point):
            raise TypeError("'pt' must be a 'Point'")
        if not isinstance(direction, Direction):
            raise TypeError("'dir' must be a 'Direction'")
        self._location = pt
        self._direction = direction
        self._ax2 = gp_Ax2(pt.pnt(), direction.dir())

    @property
    def location(self):
        """
        Location of this axis as :class:`.Point`
        """
        return self._location

    @property
    def direction(self):
        """
        Direction of this axis as :class:`.Direction`
        """
        return self._direction

    def ax2(self):
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
            self._pln = gp_Pln(pt.pnt(), normal.dir())
        else:
            raise TypeError("Wrong argument types")

    @property
    def location(self):
        """
        Location of this plane
        """
        return self._location

    def pln(self):
        """
        Get the underlying OpenCascade object

        :return: The underlying OpenCascade object
        """
        return self._pln

    @classmethod
    def from_pln(cls, pln):
        """
        Construct ``figura`` object from an OpenCascade ``gp_Pln`` object

        :param pln: OpenCascade ``gp_Pln`` object
        :return: :class:`.Plane` object
        """
        pt = figura.shapes.Point.from_pnt(pln.Location())
        normal = Direction.from_dir(pln.Axis().Direction())
        return Plane(pt, normal)
