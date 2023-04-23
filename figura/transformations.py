from OCC.Core.gp import (
    gp_Trsf
)
from OCC.Core.BRepBuilderAPI import (
    BRepBuilderAPI_Transform
)
from .geometry import Axis1


class Transformation(object):

    def __init__(self):
        pass


class Mirror(Transformation):

    def __init__(self, axis1):
        super().__init__()
        self._trsf = None
        if isinstance(axis1, Axis1):
            self._trsf = gp_Trsf()
            self._trsf.SetMirror(axis1.ax1())
        else:
            raise SystemError("axis1 must be 'Axis1'")

    def do(self, shape):
        brep_trsf = BRepBuilderAPI_Transform(shape.shape(), self._trsf)
        return brep_trsf.Shape()
