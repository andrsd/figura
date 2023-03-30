from OCC.Core.BRepPrimAPI import (
    BRepPrimAPI_MakeBox,
    BRepPrimAPI_MakeCylinder,
    BRepPrimAPI_MakeSphere,
    BRepPrimAPI_MakePrism,
    BRepPrimAPI_MakeCone
)
from OCC.Core.TopoDS import (
    TopoDS_Shape
)
from .geometry import (
    Axis2
)
from .shapes import (Shape)


class Box(Shape):
    """
    Box
    """

    def __init__(self, pt1, pt2):
        """
        Construct a box from 2 corner points

        :param pt1: First corner :class:`.Point`
        :param pt2: Second corner :class:`.Point`
        """
        self._box = BRepPrimAPI_MakeBox(pt1.obj(), pt2.obj())
        self._box.Build()
        if not self._box.IsDone():
            raise SystemExit("Box was not created")  # pragma: no cover
        super().__init__(self._box.Shape())

    def shell(self):
        """
        Get the underlying OpenCascade object that represent the shell of this box

        :return: Underlying OpenCascade object
        """
        return self._box.Shell()


class Cylinder(Shape):

    def __init__(self, axis, radius, height):
        self._cylinder = BRepPrimAPI_MakeCylinder(axis.obj(), radius, height)
        self._cylinder.Build()
        if not self._cylinder.IsDone():
            raise SystemExit("Cylinder was not created")  # pragma: no cover
        super().__init__(self._cylinder.Shape())

    def shell(self):
        return self._cylinder.Shell()

    def solid(self):
        return self._cylinder.Solid()


class Sphere(Shape):

    def __init__(self, center, radius):
        self._sphere = BRepPrimAPI_MakeSphere(center.obj(), radius)
        self._sphere.Build()
        if not self._sphere.IsDone():
            raise SystemExit("Sphere was not created")  # pragma: no cover
        super().__init__(self._sphere.Shape())

    def shell(self):
        return self._sphere.Shell()

    def solid(self):
        return self._sphere.Solid()


class Prism(Shape):

    def __init__(self, shape, vec):
        if not hasattr(shape, "obj"):
            raise SystemExit("'shape' must have a 'obj' method")
        shp = shape.obj()
        if not isinstance(shp, TopoDS_Shape):
            raise SystemExit("'shape' is not a TopoDS_Shape")
        self._prism = BRepPrimAPI_MakePrism(shp, vec.obj())
        self._prism.Build()
        if not self._prism.IsDone():
            raise SystemExit("Prism was not created")  # pragma: no cover
        super().__init__(self._prism.Shape())


class Cone(Shape):

    def __init__(self, axis, radius1, radius2, height):
        if not isinstance(axis, Axis2):
            raise TypeError("'axis' must be a Axis2")
        self._cone = BRepPrimAPI_MakeCone(axis.obj(), radius1, radius2, height)
        self._cone.Build()
        if not self._cone.IsDone():
            raise SystemExit("Cone was not created")  # pragma: no cover
        super().__init__(self._cone.Shape())

    def shell(self):
        return self._cone.Shell()

    def solid(self):
        return self._cone.Solid()
