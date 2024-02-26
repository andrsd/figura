from OCC.Core.gp import (
    gp_Vec2d,
    gp_Dir2d,
    gp_Ax2d,
    gp_Ax22d
)
import figura.d2


class Geometry(object):

    def __init__(self):
        self.shape = None

    @staticmethod
    def OX():
        pt = figura.d2.Point(0, 0)
        direction = Direction(1, 0)
        return Axis(pt, direction)

    @staticmethod
    def OY():
        pt = figura.d2.Point(0, 0)
        direction = Direction(0, 1)
        return Axis(pt, direction)

    @staticmethod
    def DX():
        return Direction(1, 0)

    @staticmethod
    def DY():
        return Direction(0, 1)


class Vector(object):
    """
    Non-persistent vector in 2D space
    """

    def __init__(self, x, y):
        """
        Creates a point with its three cartesian coordinates.

        :param x: x-coordinate
        :param y: y-coordinate
        """
        self._vec = gp_Vec2d(x, y)

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

    def vec(self):
        """
        Get the underlying OpenCascade object

        :return: The underlying OpenCascade object
        """
        return self._vec

    @classmethod
    def from_vec(cls, vec):
        """
        Construct ``figura`` object from an OpenCascade ``gp_Vec2d`` object

        :param vec: OpenCascade ``gp_Vec2d`` object
        :return: :class:`.Vector` object
        """
        return Vector(vec.X(), vec.Y())

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __str__(self):
        return "{}(x={}, y={})".format(self.__class__, self.x, self.y)


class Direction(object):
    """
    Describes a unit vector in 2D space. This unit vector is also called
    "Direction".
    """

    def __init__(self, x, y):
        """
        Creates a direction with its 2 cartesian coordinates.

        :param x: x-coordinate
        :param y: y-coordinate
        """
        self._dir = gp_Dir2d(x, y)

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

    def dir(self):
        """
        Get the underlying OpenCascade object

        :return: The underlying OpenCascade object
        """
        return self._dir

    @classmethod
    def from_dir(cls, dir):
        """
        Construct ``figura`` object from an OpenCascade ``gp_Dir2d`` object

        :param dir: OpenCascade ``gp_Dir2d`` object
        :return: :class:`.Direction` object
        """
        return Direction(dir.X(), dir.Y())

    def __neg__(self):
        return Direction(-self.x, -self.y)

    def __str__(self):
        return "{}(x={}, y={})".format(self.__class__, self.x, self.y)


class Axis(object):

    def __init__(self, pt, direction):
        """
        Describes an axis in 2D space. An axis is defined by:

        - its origin (also referred to as its "Location point"), and
        - its unit vector (referred to as its "Direction").

        An axis implicitly defines a direct, right-handed coordinate system in
        2D space by:

        - its origin,
        - its "Direction" (giving the "X Direction" of the coordinate system),
          and
        - the unit vector normal to "Direction" (positive angle measured in
          the trigonometric sense)

        An axis is used:

        - to describe 2D geometric entities (for example, the axis which
          defines angular coordinates on a circle). It serves for the same
          purpose as the STEP function "axis placement one axis", or
        - to define geometric transformations (axis of symmetry, axis of
          rotation, and so on).

        Note: to define a left-handed 2D coordinate system, use Axis2.

        :param pt: :class:`.Point` the location point
        :param direction: :class:`.Direction` the direction of the axis
        """
        if not isinstance(pt, figura.d2.Point):
            raise TypeError("'pt' must be a 'Point'")
        if not isinstance(direction, Direction):
            raise TypeError("'dir' must be a 'Direction'")
        self._location = pt
        self._direction = direction
        self._ax = gp_Ax2d(pt.pnt(), direction.dir())

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

    def ax(self):
        """
        Get the underlying OpenCascade object

        :return: The underlying OpenCascade object
        """
        return self._ax


class Axis2(object):
    """
    Describes a coordinate system in a plane (2D space). A coordinate system is
    defined by:

    - its origin (also referred to as its "Location point"), and
    - two orthogonal unit vectors, respectively, called the "X Direction" and
      the "Y Direction".

    An `Axis2` may be right-handed ("direct sense") or left-handed ("inverse"
    or "indirect sense"). You use an Axis2 to:

    - describe 2D geometric entities, in particular to position them. The local
      coordinate system of a geometric entity serves for the same purpose as
      the STEP function "axis placement two axes", or
    - define geometric transformations.

    Note: we refer to the "X Axis" and "Y Axis" as the axes having:
    - the origin of the coordinate system as their origin, and
    - the unit vectors "X Direction" and "Y Direction", respectively, as their
      unit vectors.
    """

    def __init__(self, pt, direction, sense=True):
        if not isinstance(pt, figura.d2.Point):
            raise TypeError("'pt' must be a 'Point'")
        if not isinstance(direction, Direction):
            raise TypeError("'dir' must be a 'Direction'")
        self._location = pt
        self._direction = direction
        self._ax2 = gp_Ax22d(pt.pnt(), direction.dir(), sense)

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
