import OCC.Core.STEPControl as step
from OCC.Core.gp import (
    gp_Pnt,
    gp_Vec,
    gp_Dir,
    gp_Ax2
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


class Point(object):
    """
    Defines 3D cartesian point
    """

    def __init__(self, x, y, z):
        self._pnt = gp_Pnt(x, y, z)

    @property
    def x(self):
        return self._pnt.X()

    @property
    def y(self):
        return self._pnt.Y()

    @property
    def z(self):
        return self._pnt.Z()

    def obj(self):
        return self._pnt


class Vector(object):
    """
    Non-persistent vector in 3D space
    """

    def __init__(self, x, y, z):
        self._vec = gp_Vec(x, y, z)

    @property
    def x(self):
        return self._vec.X()

    @property
    def y(self):
        return self._vec.Y()

    @property
    def z(self):
        return self._vec.Z()

    def obj(self):
        return self._vec


class Direction(object):
    """
    Describes a unit vector in 3D space
    """

    def __init__(self, x, y, z):
        self._dir = gp_Dir(x, y, z)

    @property
    def x(self):
        return self._dir.X()

    @property
    def y(self):
        return self._dir.Y()

    @property
    def z(self):
        return self._dir.Z()

    def obj(self):
        return self._dir


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
        return self._location

    @property
    def direction(self):
        return self._direction

    def obj(self):
        return self._ax2
