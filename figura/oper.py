from figura.shapes import Shape, Face, Plane, Wire
from figura.geometry import (Axis1)
from OCC.Core.BRepBuilderAPI import (
    BRepBuilderAPI_MakeWire
)
from OCC.Core.BRepAlgoAPI import (
    BRepAlgoAPI_Fuse,
    BRepAlgoAPI_Cut,
    BRepAlgoAPI_Common,
    BRepAlgoAPI_Section
)
from OCC.Core.TopTools import TopTools_ListOfShape
from OCC.Core.BRepOffsetAPI import (
    BRepOffsetAPI_MakeThickSolid
)
from OCC.Core.BRepPrimAPI import (
    BRepPrimAPI_MakePrism,
    BRepPrimAPI_MakeRevol
)
from OCC.Core.BRepFilletAPI import BRepFilletAPI_MakeFillet
import math


def fuse(shape, tool):
    """
    Boolean fusion operation between arguments and tools (Boolean Union)

    :param shape: Argument
    :param tool: Tool
    :return: Shape resulting from the fusion operation
    """
    if hasattr(tool, 'shape'):
        result = BRepAlgoAPI_Fuse(shape.shape(), tool.shape())
        result.Build()
        result.SimplifyResult()
        if not result.IsDone():
            raise SystemExit("Objects were not fused")  # pragma: no cover
        return Shape.from_shape(result.Shape())
    else:
        raise TypeError("`shape` object does not have `shape()` method")


def cut(shape, tool):
    if hasattr(tool, 'shape'):
        result = BRepAlgoAPI_Cut(shape.shape(), tool.shape())
        result.Build()
        if not result.IsDone():
            raise SystemExit("Object was not cut")  # pragma: no cover
        return Shape.from_shape(result.Shape())
    else:
        raise TypeError("`tool` object does not have `shape()` method")


def intersect(shape, tool):
    if hasattr(tool, 'shape'):
        result = BRepAlgoAPI_Common(shape.shape(), tool.shape())
        result.Build()
        if not result.IsDone():
            raise SystemExit("Object was not intersected")  # pragma: no cover
        return Shape.from_shape(result.Shape())
    else:
        raise TypeError("`tool` object does not have `shape()` method")


def fillet(shape, edges, radius):
    result = BRepFilletAPI_MakeFillet(shape.shape())
    for e in edges:
        result.Add(radius, e.shape())
    return Shape.from_shape(result.Shape())


def hollow(shape, faces_to_remove, thickness, tolerance):
    # TODO: check that `faces_to_remove` is a iterable object
    rem_faces = TopTools_ListOfShape()
    for face in faces_to_remove:
        if isinstance(face, Face):
            rem_faces.Append(face.shape())

    result = BRepOffsetAPI_MakeThickSolid()
    result.MakeThickSolidByJoin(shape.shape(), rem_faces, thickness,
                                tolerance)
    result.Build()
    return Shape.from_shape(result.Shape())


def extrude(shape, vec):
    result = BRepPrimAPI_MakePrism(shape.shape(), vec.vec())
    result.Build()
    if not result.IsDone():
        raise SystemExit("extrude failed")  # pragma: no cover
    return Shape.from_shape(result.Shape())


def revolve(shape, axis, angle=2. * math.pi):
    if isinstance(axis, Axis1):
        result = BRepPrimAPI_MakeRevol(shape.shape(), axis.ax1(), angle)
        result.Build()
        if not result.IsDone():
            raise SystemExit("revolve failed")  # pragma: no cover
        return Shape.from_shape(result.Shape())
    else:
        raise TypeError("Wrong argument types")


def section(shape: Shape, plane: Plane):
    """
    Compute section between a shape and a plane

    :param shape: Shape
    :param plane: Plane
    :return: Wire that forms the computed section
    """
    result = BRepAlgoAPI_Section(shape.shape(), plane.pln())
    result.Build()
    if not result.IsDone():
        raise SystemExit("Section operation failed")  # pragma: no cover
    section_edges = result.SectionEdges();
    wire = BRepBuilderAPI_MakeWire()
    wire.Add(section_edges)
    wire.Build()
    if not wire.IsDone():
        raise SystemExit("Wire was not created")  # pragma: no cover
    return Wire.from_shape(wire.Wire())
