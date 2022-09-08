from OCC.Core.BRepPrimAPI import (
    BRepPrimAPI_MakeBox,
    BRepPrimAPI_MakeCylinder,
    BRepPrimAPI_MakeSphere,
    BRepPrimAPI_MakePrism,
    BRepPrimAPI_MakeCone
)
from OCC.Core.BRepAlgoAPI import (
    BRepAlgoAPI_Fuse
)
from OCC.Core.TopoDS import (
    TopoDS_Shape
)
from .geometry import (
    Axis2
)
from .shapes import (Shape)


class Primitive(object):

    def __init__(self):
        self._name = None

    def name(self, value=None):
        if value is None:
            return self._name
        elif isinstance(value, str):
            self._name = value
        else:
            raise TypeError("'value' must be a 'string'.")

    def shape(self):
        raise NotImplementedError()

    def fuse(self, shape):
        fuse = None
        if hasattr(shape, 'shape'):
            fuse = BRepAlgoAPI_Fuse(self.shape(), shape.shape())
        else:
            raise TypeError("Wrong argument types")

        fuse.Build()
        if not fuse.IsDone():
            raise SystemExit("Objects were not fused")
        return Shape.from_obj(fuse.Shape())


class Box(Primitive):
    """
    Box
    """

    def __init__(self, pt1, pt2):
        super().__init__()
        self._box = BRepPrimAPI_MakeBox(pt1.obj(), pt2.obj())
        self._box.Build()
        if not self._box.IsDone():
            raise SystemExit("Box was not created")

    def shell(self):
        return self._box.Shell()

    def solid(self):
        return self._box.Solid()

    def shape(self):
        return self._box.Shape()


class Cylinder(Primitive):

    def __init__(self, axis, radius, height):
        super().__init__()
        self._cylinder = BRepPrimAPI_MakeCylinder(axis.obj(), radius, height)
        self._cylinder.Build()
        if not self._cylinder.IsDone():
            raise SystemExit("Cylinder was not created")

    def shell(self):
        return self._cylinder.Shell()

    def solid(self):
        return self._cylinder.Solid()

    def shape(self):
        return self._cylinder.Shape()


class Sphere(Primitive):

    def __init__(self, center, radius):
        super().__init__()
        self._sphere = BRepPrimAPI_MakeSphere(center.obj(), radius)
        self._sphere.Build()
        if not self._sphere.IsDone():
            raise SystemExit("Sphere was not created")

    def shell(self):
        return self._sphere.Shell()

    def solid(self):
        return self._sphere.Solid()

    def shape(self):
        return self._sphere.Shape()


class Prism(Primitive):

    def __init__(self, shape, vec):
        super().__init__()
        if not hasattr(shape, "obj"):
            raise SystemExit("'shape' must have a 'obj' method")
        shp = shape.obj()
        if not isinstance(shp, TopoDS_Shape):
            raise SystemExit("'shape' is not a TopoDS_Shape")
        self._prism = BRepPrimAPI_MakePrism(shp, vec.obj())
        self._prism.Build()
        if not self._prism.IsDone():
            raise SystemExit("Prism was not created")

    def shape(self):
        return self._prism.Shape()


class Cone(Primitive):

    def __init__(self, axis, radius1, radius2, height):
        super().__init__()
        if not isinstance(axis, Axis2):
            raise TypeError("'axis' must be a Axis2")
        self._cone = BRepPrimAPI_MakeCone(axis.obj(), radius1, radius2, height)
        self._cone.Build()
        if not self._cone.IsDone():
            raise SystemExit("Cone was not created")

    def shell(self):
        return self._cone.Shell()

    def solid(self):
        return self._cone.Solid()

    def shape(self):
        return self._cone.Shape()
