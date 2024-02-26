import pytest
from pathlib import Path
import os
from figura.io import (
    STEPFile,
    STLFile
)
from figura.d3 import *


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


def test_step_write(tmp_path):
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 1)
    box = Box(pt1, pt2)

    step = STEPFile(os.path.join(Path(tmp_path), "cube.step"))
    step.write([box])


def test_stl_write(tmp_path):
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 1)
    box = Box(pt1, pt2)

    stl = STLFile(os.path.join(Path(tmp_path), "cube"))
    stl.write([box])


def test_stl_write_named(tmp_path):
    pt1 = Point(0, 0, 0)
    pt2 = Point(1, 1, 1)
    box = Box(pt1, pt2)
    box.name = "name"

    stl = STLFile(os.path.join(Path(tmp_path), "cube.stl"))
    stl.write([box])
