import pytest
import os
from figura.io import (
    STEPFile,
    STLFile
)
from figura.primitives import (
    Box
)
from figura.shapes import (
    Point
)


assets_dir = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "assets"
)


def test_step_read():
    step = STEPFile(os.path.join(assets_dir, "cube.step"))
    step.read()


def test_step_read_non_existent():
    with pytest.raises(SystemExit):
        step = STEPFile(os.path.join(assets_dir, "non-existent.step"))
        step.read()


def test_step_write():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 1)
    box = Box(pt1, pt2)

    step = STEPFile(os.path.join("cube.step"))
    step.write([box])


def test_stl_write():
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 1)
    box = Box(pt1, pt2)

    stl = STLFile(os.path.join("cube"))
    stl.write([box])
