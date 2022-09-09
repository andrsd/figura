import OCC.Core.STEPControl as step
from OCC.Core.gp import (
    gp_Pnt,
    gp_Vec,
    gp_Dir,
    gp_Ax1,
    gp_Ax2,
    gp_OX,
    gp_OY,
    gp_OZ,
    gp_DX,
    gp_DY,
    gp_DZ
)
from OCC.Core.IFSelect import IFSelect_RetDone


class Geometry(object):

    def __init__(self):
        self.shape = None

    def write(self, file_name, format="STEP"):
        if format == "STEP":
            self._write_step_file(file_name)
        else:
            raise SystemError("Unknown format '{}'".format(format))

    def read(self, file_name, format="STEP"):
        if format == "STEP":
            self._read_step_file(file_name)
        else:
            raise SystemError("Unknown format '{}'".format(format))

    def _read_step_file(self, file_name):
        step_reader = step.STEPControl_Reader()
        if step_reader.ReadFile(file_name) != IFSelect_RetDone:
            raise SystemExit("Unable to load '{}'".format(file_name))
        step_reader.NbRootsForTransfer()
        step_reader.TransferRoot()
        self.shape = step_reader.OneShape()

    def _write_step_file(self, file_name):
        step_writer = step.STEPControl_Writer()
        step_writer.Transfer(self.shape, step.STEPControl_AsIs)
        step_writer.Write(file_name)

    @staticmethod
    def OX():
        ax1 = gp_OX()
        pt = Point.from_obj(ax1.Location())
        dir = Direction.from_obj(ax1.Direction())
        return Axis1(pt, dir)

    @staticmethod
    def OY():
        ax1 = gp_OY()
        pt = Point.from_obj(ax1.Location())
        dir = Direction.from_obj(ax1.Direction())
        return Axis1(pt, dir)

    @staticmethod
    def OZ():
        ax1 = gp_OZ()
        pt = Point.from_obj(ax1.Location())
        dir = Direction.from_obj(ax1.Direction())
        return Axis1(pt, dir)

    @staticmethod
    def DX():
        dir = gp_DX()
        return Direction.from_obj(dir)

    @staticmethod
    def DY():
        dir = gp_DY()
        return Direction.from_obj(dir)

    @staticmethod
    def DZ():
        dir = gp_DZ()
        return Direction.from_obj(dir)


class Point(object):
    """
    Defines 3D cartesian point
    """

    def __init__(self, x, y, z):
        """
        Construct a 3D point from its coordinates

        :param x: X-coordinate
        :param y: Y-coordinate
        :param z: Z-coordinate
        """
        self._pnt = gp_Pnt(x, y, z)

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

    def obj(self):
        """
        Get the underlying OpenCascade object

        :return: The underlying OpenCascade object
        """
        return self._pnt

    @classmethod
    def from_obj(cls, obj):
        """
        Construct ``figura`` object from an OpenCascade ``gp_Pnt`` object

        :param obj: OpenCascade ``gp_Pnt`` object
        :return: :class:`.Point` object
        """
        return Point(obj.X(), obj.Y(), obj.Z())

    def __str__(self):
        return "{}(x={}, y={}, z={})".format(
            self.__class__, self.x, self.y, self.z)


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

    def __str__(self):
        return "{}(x={}, y={}, z={})".format(
            self.__class__, self.x, self.y, self.z)


class Axis1(object):

    def __init__(self, pt, dir):
        if not isinstance(pt, Point):
            raise TypeError("'pt' must be a 'Point'")
        if not isinstance(dir, Direction):
            raise TypeError("'dir' must be a 'Direction'")
        self._location = pt
        self._direction = dir
        self._ax1 = gp_Ax1(pt.obj(), dir.obj())

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

    def __init__(self, pt, dir):
        if not isinstance(pt, Point):
            raise TypeError("'pt' must be a 'Point'")
        if not isinstance(dir, Direction):
            raise TypeError("'dir' must be a 'Direction'")
        self._location = pt
        self._direction = dir
        self._ax2 = gp_Ax2(pt.obj(), dir.obj())

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
